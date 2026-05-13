from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class PublicCollection(BaseModel):
    resource: Literal["proposals", "resolutions", "correspondence"]
    status: Literal["skeleton"]
    items: list[dict]


@router.get("/public/proposals", response_model=PublicCollection)
async def list_public_proposals() -> PublicCollection:
    return PublicCollection(resource="proposals", status="skeleton", items=[])


@router.get("/public/resolutions", response_model=PublicCollection)
async def list_public_resolutions() -> PublicCollection:
    return PublicCollection(resource="resolutions", status="skeleton", items=[])


@router.get("/public/correspondence", response_model=PublicCollection)
async def list_public_correspondence() -> PublicCollection:
    return PublicCollection(resource="correspondence", status="skeleton", items=[])

