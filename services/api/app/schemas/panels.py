from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class CreatePanelRequest(BaseModel):
    proposal_id: str
    sortition_run_id: str
    title: str = Field(min_length=10, max_length=240)
    mandate_summary: str = Field(min_length=20, max_length=2000)


class PanelMandateResponse(BaseModel):
    id: str
    member_id: str
    sortition_result_id: str
    role: str
    status: str
    created_at: datetime


class ResolutionResponse(BaseModel):
    id: str
    panel_id: str
    proposal_id: str
    title: str
    body_markdown: str
    status: str
    decision_method: str
    published_at: datetime | None
    created_at: datetime


class PanelResponse(BaseModel):
    id: str
    proposal_id: str
    sortition_run_id: str
    arena_id: str
    title: str
    mandate_summary: str
    status: str
    created_at: datetime
    mandates: list[PanelMandateResponse]
    resolutions: list[ResolutionResponse]


class CreatePanelResponse(BaseModel):
    panel: PanelResponse
    journal_entry_id: str
    journal_entry_hash: str


class CreateResolutionRequest(BaseModel):
    title: str = Field(min_length=10, max_length=240)
    body_markdown: str = Field(min_length=50)
    status: Literal["draft", "published"] = "published"
    decision_method: str = Field(default="pilot_consensus", max_length=80)


class CreateResolutionResponse(BaseModel):
    resolution: ResolutionResponse
    journal_entry_id: str
    journal_entry_hash: str


class PublicResolutionCollection(BaseModel):
    resource: Literal["resolutions"] = "resolutions"
    status: Literal["live"] = "live"
    items: list[ResolutionResponse]
