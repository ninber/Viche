from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.proposals import list_submitted_proposals
from app.db.models import Resolution
from app.db.session import get_db
from app.schemas.panels import PublicResolutionCollection, ResolutionResponse
from app.schemas.proposals import PublicProposalCollection

router = APIRouter()
DbSession = Annotated[AsyncSession, Depends(get_db)]


class PublicCollection(BaseModel):
    resource: Literal["correspondence"]
    status: Literal["skeleton"]
    items: list[dict]


@router.get("/public/proposals", response_model=PublicProposalCollection)
async def list_public_proposals(
    session: DbSession,
) -> PublicProposalCollection:
    return PublicProposalCollection(items=await list_submitted_proposals(session))


@router.get("/public/resolutions", response_model=PublicResolutionCollection)
async def list_public_resolutions(session: DbSession) -> PublicResolutionCollection:
    resolutions = (
        await session.scalars(
            select(Resolution)
            .where(Resolution.status == "published")
            .order_by(Resolution.created_at.desc())
            .limit(20)
        )
    ).all()
    return PublicResolutionCollection(
        items=[
            ResolutionResponse(
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
            for resolution in resolutions
        ]
    )


@router.get("/public/correspondence", response_model=PublicCollection)
async def list_public_correspondence() -> PublicCollection:
    return PublicCollection(resource="correspondence", status="skeleton", items=[])
