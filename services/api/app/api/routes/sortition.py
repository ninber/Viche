from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    EligibilityPool,
    EligibilityPoolMember,
    Member,
    PublicIdentity,
    SortitionResult,
    SortitionRun,
)
from app.db.session import get_db
from app.domain.journal import append_journal_entry, canonical_json, sha256_digest
from app.schemas.sortition import (
    CreateEligibilityPoolRequest,
    CreateEligibilityPoolResponse,
    EligibilityPoolResponse,
    RunSortitionRequest,
    RunSortitionResponse,
    SortitionResultResponse,
    SortitionRunResponse,
)

router = APIRouter()
DbSession = Annotated[AsyncSession, Depends(get_db)]


def pool_response(pool: EligibilityPool) -> EligibilityPoolResponse:
    return EligibilityPoolResponse(
        id=pool.id,
        arena_id=pool.arena_id,
        name=pool.name,
        status=pool.status,
        pool_hash=pool.pool_hash,
        member_count=pool.member_count,
        created_at=pool.created_at,
    )


def sortition_result_response(result: SortitionResult) -> SortitionResultResponse:
    return SortitionResultResponse(
        member_id=result.member_id,
        rank=result.rank,
        seat_type=result.seat_type,
        selection_hash=result.selection_hash,
    )


def sortition_run_response(
    run: SortitionRun,
    results: list[SortitionResult],
) -> SortitionRunResponse:
    return SortitionRunResponse(
        id=run.id,
        pool_id=run.pool_id,
        status=run.status,
        target_seats=run.target_seats,
        reserve_seats=run.reserve_seats,
        seed=run.seed,
        algorithm=run.algorithm,
        transcript_hash=run.transcript_hash,
        created_at=run.created_at,
        results=[sortition_result_response(result) for result in results],
    )


async def _eligible_members(
    session: AsyncSession,
    member_ids: list[str] | None,
) -> list[tuple[Member, PublicIdentity]]:
    statement = select(Member, PublicIdentity).join(PublicIdentity).where(Member.status == "active")
    if member_ids:
        statement = statement.where(Member.id.in_(member_ids))
    rows = (await session.execute(statement.order_by(Member.id))).all()
    return [(member, identity) for member, identity in rows]


@router.post(
    "/eligibility-pools",
    response_model=CreateEligibilityPoolResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_eligibility_pool(
    request: CreateEligibilityPoolRequest,
    session: DbSession,
) -> CreateEligibilityPoolResponse:
    eligible_members = await _eligible_members(session, request.member_ids)
    if not eligible_members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no eligible active members found",
        )

    pool_payload = {
        "arena_id": request.arena_id,
        "member_ids": [member.id for member, _identity in eligible_members],
    }
    pool = EligibilityPool(
        arena_id=request.arena_id,
        name=request.name,
        pool_hash=sha256_digest(canonical_json(pool_payload)),
        member_count=len(eligible_members),
    )
    session.add(pool)
    await session.flush()

    session.add_all(
        [
            EligibilityPoolMember(
                pool_id=pool.id,
                member_id=member.id,
                public_identity_id=identity.id,
                weight=1,
            )
            for member, identity in eligible_members
        ]
    )
    await session.flush()

    journal = await append_journal_entry(
        session,
        event_type="eligible_pool.frozen",
        actor_type="operator",
        actor_id=None,
        subject_type="eligibility_pool",
        subject_id=pool.id,
        payload={
            "pool_id": pool.id,
            "arena_id": pool.arena_id,
            "pool_hash": pool.pool_hash,
            "member_count": pool.member_count,
        },
    )
    await session.commit()

    return CreateEligibilityPoolResponse(
        pool=pool_response(pool),
        journal_entry_id=journal.id,
        journal_entry_hash=journal.entry_hash,
    )


@router.post(
    "/sortitions",
    response_model=RunSortitionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def run_sortition(
    request: RunSortitionRequest,
    session: DbSession,
) -> RunSortitionResponse:
    pool = await session.get(EligibilityPool, request.pool_id)
    if pool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pool not found")

    pool_members = (
        await session.scalars(
            select(EligibilityPoolMember)
            .where(EligibilityPoolMember.pool_id == pool.id)
            .order_by(EligibilityPoolMember.member_id)
        )
    ).all()
    needed = request.target_seats + request.reserve_seats
    if len(pool_members) < needed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="not enough pool members for requested seats",
        )

    seed = request.seed or f"{pool.pool_hash}:{datetime.now(UTC).isoformat()}"
    ranked = sorted(
        (
            (
                sha256_digest(
                    canonical_json(
                        {
                            "seed": seed,
                            "pool_hash": pool.pool_hash,
                            "member_id": pool_member.member_id,
                        }
                    )
                ),
                pool_member,
            )
            for pool_member in pool_members
        ),
        key=lambda item: item[0],
    )
    selected = ranked[:needed]
    transcript = {
        "algorithm": "sha256_member_order_v1",
        "pool_id": pool.id,
        "pool_hash": pool.pool_hash,
        "seed": seed,
        "target_seats": request.target_seats,
        "reserve_seats": request.reserve_seats,
        "selected": [
            {
                "member_id": pool_member.member_id,
                "rank": rank,
                "selection_hash": selection_hash,
            }
            for rank, (selection_hash, pool_member) in enumerate(selected, start=1)
        ],
    }
    run = SortitionRun(
        pool_id=pool.id,
        target_seats=request.target_seats,
        reserve_seats=request.reserve_seats,
        seed=seed,
        transcript_hash=sha256_digest(canonical_json(transcript)),
    )
    session.add(run)
    await session.flush()

    results = [
        SortitionResult(
            run_id=run.id,
            member_id=pool_member.member_id,
            rank=rank,
            seat_type="primary" if rank <= request.target_seats else "reserve",
            selection_hash=selection_hash,
        )
        for rank, (selection_hash, pool_member) in enumerate(selected, start=1)
    ]
    session.add_all(results)
    await session.flush()

    journal = await append_journal_entry(
        session,
        event_type="sortition.completed",
        actor_type="operator",
        actor_id=None,
        subject_type="sortition_run",
        subject_id=run.id,
        payload={
            "run_id": run.id,
            "pool_id": pool.id,
            "pool_hash": pool.pool_hash,
            "seed": run.seed,
            "algorithm": run.algorithm,
            "target_seats": run.target_seats,
            "reserve_seats": run.reserve_seats,
            "transcript_hash": run.transcript_hash,
        },
    )
    await session.commit()

    return RunSortitionResponse(
        run=sortition_run_response(run, results),
        journal_entry_id=journal.id,
        journal_entry_hash=journal.entry_hash,
    )


@router.get("/sortitions/{run_id}", response_model=SortitionRunResponse)
async def get_sortition_run(
    run_id: str,
    session: DbSession,
) -> SortitionRunResponse:
    run = await session.get(SortitionRun, run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sortition not found")
    results = (
        await session.scalars(
            select(SortitionResult)
            .where(SortitionResult.run_id == run.id)
            .order_by(SortitionResult.rank)
        )
    ).all()
    return sortition_run_response(run, list(results))
