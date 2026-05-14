from datetime import datetime

from pydantic import BaseModel, Field


class CreateEligibilityPoolRequest(BaseModel):
    arena_id: str
    name: str = Field(min_length=3, max_length=180)
    member_ids: list[str] | None = None


class EligibilityPoolResponse(BaseModel):
    id: str
    arena_id: str
    name: str
    status: str
    pool_hash: str
    member_count: int
    created_at: datetime


class CreateEligibilityPoolResponse(BaseModel):
    pool: EligibilityPoolResponse
    journal_entry_id: str
    journal_entry_hash: str


class RunSortitionRequest(BaseModel):
    pool_id: str
    target_seats: int = Field(gt=0)
    reserve_seats: int = Field(default=0, ge=0)
    seed: str | None = Field(default=None, max_length=160)


class SortitionResultResponse(BaseModel):
    member_id: str
    rank: int
    seat_type: str
    selection_hash: str


class SortitionRunResponse(BaseModel):
    id: str
    pool_id: str
    status: str
    target_seats: int
    reserve_seats: int
    seed: str
    algorithm: str
    transcript_hash: str
    created_at: datetime
    results: list[SortitionResultResponse]


class RunSortitionResponse(BaseModel):
    run: SortitionRunResponse
    journal_entry_id: str
    journal_entry_hash: str
