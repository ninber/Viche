from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.proposals import list_submitted_proposals
from app.db.session import get_db
from app.schemas.proposals import PublicProposalCollection

router = APIRouter()
DbSession = Annotated[AsyncSession, Depends(get_db)]


class PublicCollection(BaseModel):
    resource: Literal["proposals", "resolutions", "correspondence"]
    status: Literal["skeleton"]
    items: list[dict]


@router.get("/public/proposals", response_model=PublicProposalCollection)
async def list_public_proposals(
    session: DbSession,
) -> PublicProposalCollection:
    return PublicProposalCollection(items=await list_submitted_proposals(session))


@router.get("/public/resolutions", response_model=PublicCollection)
async def list_public_resolutions() -> PublicCollection:
    return PublicCollection(resource="resolutions", status="skeleton", items=[])


@router.get("/public/correspondence", response_model=PublicCollection)
async def list_public_correspondence() -> PublicCollection:
    return PublicCollection(resource="correspondence", status="skeleton", items=[])
