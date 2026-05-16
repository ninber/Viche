from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Panel, PanelMandate, Proposal, Resolution, SortitionResult, SortitionRun
from app.db.session import get_db
from app.domain.journal import append_journal_entry
from app.schemas.panels import (
    CreatePanelRequest,
    CreatePanelResponse,
    CreateResolutionRequest,
    CreateResolutionResponse,
    PanelMandateResponse,
    PanelResponse,
    ResolutionResponse,
)

router = APIRouter()
DbSession = Annotated[AsyncSession, Depends(get_db)]


def mandate_response(mandate: PanelMandate) -> PanelMandateResponse:
    return PanelMandateResponse(
        id=mandate.id,
        member_id=mandate.member_id,
        sortition_result_id=mandate.sortition_result_id,
        role=mandate.role,
        status=mandate.status,
        created_at=mandate.created_at,
    )


def resolution_response(resolution: Resolution) -> ResolutionResponse:
    return ResolutionResponse(
        id=resolution.id,
        panel_id=resolution.panel_id,
        proposal_id=resolution.proposal_id,
        title=resolution.title,
        body_markdown=resolution.body_markdown,
        status=resolution.status,
        decision_method=resolution.decision_method,
        published_at=resolution.published_at,
        created_at=resolution.created_at,
    )


def panel_response(panel: Panel) -> PanelResponse:
    return PanelResponse(
        id=panel.id,
        proposal_id=panel.proposal_id,
        sortition_run_id=panel.sortition_run_id,
        arena_id=panel.arena_id,
        title=panel.title,
        mandate_summary=panel.mandate_summary,
        status=panel.status,
        created_at=panel.created_at,
        mandates=[mandate_response(mandate) for mandate in panel.mandates],
        resolutions=[resolution_response(resolution) for resolution in panel.resolutions],
    )


async def _load_panel(session: AsyncSession, panel_id: str) -> Panel | None:
    return await session.scalar(
        select(Panel)
        .options(selectinload(Panel.mandates), selectinload(Panel.resolutions))
        .where(Panel.id == panel_id)
    )


@router.post("/panels", response_model=CreatePanelResponse, status_code=status.HTTP_201_CREATED)
async def create_panel(
    request: CreatePanelRequest,
    session: DbSession,
) -> CreatePanelResponse:
    proposal = await session.get(Proposal, request.proposal_id)
    if proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="proposal not found")

    run = await session.get(SortitionRun, request.sortition_run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sortition not found")
    if run.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sortition not completed",
        )

    existing_panel = await session.scalar(
        select(Panel).where(Panel.sortition_run_id == request.sortition_run_id)
    )
    if existing_panel is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="panel already exists for sortition",
        )

    primary_results = (
        await session.scalars(
            select(SortitionResult)
            .where(
                SortitionResult.run_id == run.id,
                SortitionResult.seat_type == "primary",
            )
            .order_by(SortitionResult.rank)
        )
    ).all()
    if not primary_results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no primary seats found",
        )

    panel = Panel(
        proposal_id=proposal.id,
        sortition_run_id=run.id,
        arena_id=proposal.arena_id,
        title=request.title,
        mandate_summary=request.mandate_summary,
    )
    session.add(panel)
    await session.flush()

    mandates = [
        PanelMandate(
            panel_id=panel.id,
            member_id=result.member_id,
            sortition_result_id=result.id,
            role="member",
            status="active",
            starts_at=datetime.now(UTC),
        )
        for result in primary_results
    ]
    session.add_all(mandates)
    await session.flush()

    journal = await append_journal_entry(
        session,
        event_type="panel.created",
        actor_type="operator",
        actor_id=None,
        subject_type="panel",
        subject_id=panel.id,
        payload={
            "panel_id": panel.id,
            "proposal_id": proposal.id,
            "sortition_run_id": run.id,
            "mandate_count": len(mandates),
            "status": panel.status,
        },
    )
    await session.commit()

    loaded_panel = await _load_panel(session, panel.id)
    if loaded_panel is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="panel missing",
        )
    return CreatePanelResponse(
        panel=panel_response(loaded_panel),
        journal_entry_id=journal.id,
        journal_entry_hash=journal.entry_hash,
    )


@router.get("/panels/{panel_id}", response_model=PanelResponse)
async def get_panel(panel_id: str, session: DbSession) -> PanelResponse:
    panel = await _load_panel(session, panel_id)
    if panel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="panel not found")
    return panel_response(panel)


@router.post(
    "/panels/{panel_id}/resolutions",
    response_model=CreateResolutionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_resolution(
    panel_id: str,
    request: CreateResolutionRequest,
    session: DbSession,
) -> CreateResolutionResponse:
    panel = await session.get(Panel, panel_id)
    if panel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="panel not found")

    published_at = datetime.now(UTC) if request.status == "published" else None
    resolution = Resolution(
        panel_id=panel.id,
        proposal_id=panel.proposal_id,
        title=request.title,
        body_markdown=request.body_markdown,
        status=request.status,
        decision_method=request.decision_method,
        published_at=published_at,
    )
    session.add(resolution)
    await session.flush()

    journal = await append_journal_entry(
        session,
        event_type=(
            "resolution.published" if request.status == "published" else "resolution.drafted"
        ),
        actor_type="panel",
        actor_id=panel.id,
        subject_type="resolution",
        subject_id=resolution.id,
        payload={
            "resolution_id": resolution.id,
            "panel_id": panel.id,
            "proposal_id": panel.proposal_id,
            "status": resolution.status,
            "decision_method": resolution.decision_method,
            "published_at": (
                resolution.published_at.isoformat() if resolution.published_at else None
            ),
        },
    )
    await session.commit()

    return CreateResolutionResponse(
        resolution=resolution_response(resolution),
        journal_entry_id=journal.id,
        journal_entry_hash=journal.entry_hash,
    )
