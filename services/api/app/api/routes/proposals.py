from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Member, Proposal
from app.db.session import get_db
from app.domain.journal import append_journal_entry
from app.schemas.proposals import ProposalResponse, SubmitProposalRequest, SubmitProposalResponse

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
