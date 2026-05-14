from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Member, Proposal, ProposalRelation
from app.db.session import get_db
from app.domain.journal import append_journal_entry
from app.schemas.proposals import (
    CreateProposalRelationRequest,
    CreateProposalRelationResponse,
    ModerateProposalRequest,
    ModerateProposalResponse,
    ProposalRelationResponse,
    ProposalResponse,
    SubmitProposalRequest,
    SubmitProposalResponse,
)

router = APIRouter()
DbSession = Annotated[AsyncSession, Depends(get_db)]


def proposal_response(proposal: Proposal) -> ProposalResponse:
    return ProposalResponse(
        id=proposal.id,
        submitter_member_id=proposal.submitter_member_id,
        arena_id=proposal.arena_id,
        title=proposal.title,
        body_markdown=proposal.body_markdown,
        country_code=proposal.country_code,
        region_code=proposal.region_code,
        district_code=proposal.district_code,
        community_code=proposal.community_code,
        status=proposal.status,
        tags=proposal.tags,
        created_at=proposal.created_at,
    )


def relation_response(relation: ProposalRelation) -> ProposalRelationResponse:
    return ProposalRelationResponse(
        id=relation.id,
        source_proposal_id=relation.source_proposal_id,
        target_proposal_id=relation.target_proposal_id,
        relation_type=relation.relation_type,
        rationale=relation.rationale,
        created_at=relation.created_at,
    )


@router.post(
    "/proposals",
    response_model=SubmitProposalResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_proposal(
    request: SubmitProposalRequest,
    session: DbSession,
) -> SubmitProposalResponse:
    member = await session.get(Member, request.submitter_member_id)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submitter not found")

    proposal = Proposal(
        submitter_member_id=member.id,
        arena_id=request.arena_id,
        title=request.title,
        body_markdown=request.body_markdown,
        country_code=request.jurisdiction.country_code,
        region_code=request.jurisdiction.region_code,
        district_code=request.jurisdiction.district_code,
        community_code=request.jurisdiction.community_code,
        tags=request.tags,
    )
    session.add(proposal)
    await session.flush()

    journal = await append_journal_entry(
        session,
        event_type="proposal.submitted",
        actor_type="member",
        actor_id=member.id,
        subject_type="proposal",
        subject_id=proposal.id,
        payload={
            "proposal_id": proposal.id,
            "submitter_member_id": member.id,
            "arena_id": proposal.arena_id,
            "title": proposal.title,
            "jurisdiction": {
                "country_code": proposal.country_code,
                "region_code": proposal.region_code,
                "district_code": proposal.district_code,
                "community_code": proposal.community_code,
            },
            "tags": proposal.tags,
        },
    )
    await session.commit()

    return SubmitProposalResponse(
        proposal=proposal_response(proposal),
        journal_entry_id=journal.id,
        journal_entry_hash=journal.entry_hash,
    )


async def list_submitted_proposals(session: AsyncSession) -> list[ProposalResponse]:
    result = await session.scalars(
        select(Proposal).where(Proposal.status == "submitted").order_by(Proposal.created_at.desc())
    )
    return [proposal_response(proposal) for proposal in result.all()]


@router.patch("/proposals/{proposal_id}/moderation", response_model=ModerateProposalResponse)
async def moderate_proposal(
    proposal_id: str,
    request: ModerateProposalRequest,
    session: DbSession,
) -> ModerateProposalResponse:
    proposal = await session.get(Proposal, proposal_id)
    if proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="proposal not found")

    previous_status = proposal.status
    proposal.status = request.status

    journal = await append_journal_entry(
        session,
        event_type="proposal.moderated",
        actor_type="operator",
        actor_id=request.actor_id,
        subject_type="proposal",
        subject_id=proposal.id,
        payload={
            "proposal_id": proposal.id,
            "previous_status": previous_status,
            "status": proposal.status,
            "rationale": request.rationale,
        },
    )
    await session.commit()

    return ModerateProposalResponse(
        proposal=proposal_response(proposal),
        journal_entry_id=journal.id,
        journal_entry_hash=journal.entry_hash,
    )


@router.post(
    "/proposals/{proposal_id}/relations",
    response_model=CreateProposalRelationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_proposal_relation(
    proposal_id: str,
    request: CreateProposalRelationRequest,
    session: DbSession,
) -> CreateProposalRelationResponse:
    source = await session.get(Proposal, proposal_id)
    target = await session.get(Proposal, request.target_proposal_id)
    if source is None or target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="proposal not found")
    if source.id == target.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="proposal cannot relate to itself",
        )

    relation = ProposalRelation(
        source_proposal_id=source.id,
        target_proposal_id=target.id,
        relation_type=request.relation_type,
        rationale=request.rationale,
    )
    session.add(relation)
    await session.flush()

    journal = await append_journal_entry(
        session,
        event_type="proposal.relation.created",
        actor_type="operator",
        actor_id=None,
        subject_type="proposal_relation",
        subject_id=relation.id,
        payload={
            "source_proposal_id": relation.source_proposal_id,
            "target_proposal_id": relation.target_proposal_id,
            "relation_type": relation.relation_type,
            "rationale": relation.rationale,
        },
    )
    await session.commit()

    return CreateProposalRelationResponse(
        relation=relation_response(relation),
        journal_entry_id=journal.id,
        journal_entry_hash=journal.entry_hash,
    )


@router.get("/proposals/{proposal_id}/relations", response_model=list[ProposalRelationResponse])
async def list_proposal_relations(
    proposal_id: str,
    session: DbSession,
) -> list[ProposalRelationResponse]:
    result = await session.scalars(
        select(ProposalRelation)
        .where(ProposalRelation.source_proposal_id == proposal_id)
        .order_by(ProposalRelation.created_at.desc())
    )
    return [relation_response(relation) for relation in result.all()]
