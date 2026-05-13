from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class JurisdictionInput(BaseModel):
    country_code: str = Field(default="UA", min_length=2, max_length=2)
    region_code: str | None = None
    district_code: str | None = None
    community_code: str | None = None


class SubmitProposalRequest(BaseModel):
    submitter_member_id: str
    arena_id: str
    title: str = Field(min_length=10, max_length=240)
    body_markdown: str = Field(min_length=50)
    jurisdiction: JurisdictionInput
    tags: list[str] = Field(default_factory=list, max_length=20)


class ProposalResponse(BaseModel):
    id: str
    submitter_member_id: str
    arena_id: str
    title: str
    body_markdown: str
    country_code: str
    region_code: str | None
    district_code: str | None
    community_code: str | None
    status: str
    tags: list[str]
    created_at: datetime


class SubmitProposalResponse(BaseModel):
    proposal: ProposalResponse
    journal_entry_id: str
    journal_entry_hash: str


class PublicProposalCollection(BaseModel):
    resource: Literal["proposals"] = "proposals"
    status: Literal["live"] = "live"
    items: list[ProposalResponse]

