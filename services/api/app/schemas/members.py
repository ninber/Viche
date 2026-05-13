from datetime import datetime

from pydantic import BaseModel, Field


class ConsentInput(BaseModel):
    privacy_notice_version: str = Field(min_length=1)
    terms_version: str = Field(min_length=1)
    public_profile_opt_in: bool = False


class RegisterMemberRequest(BaseModel):
    display_locale: str = "uk-UA"
    assurance_method: str = "self_declared"
    public_display_name: str | None = Field(default=None, max_length=160)
    consents: ConsentInput


class PublicIdentityResponse(BaseModel):
    id: str
    handle: str
    display_name: str | None


class MemberResponse(BaseModel):
    id: str
    display_locale: str
    assurance_level: str
    status: str
    public_identity: PublicIdentityResponse
    created_at: datetime


class RegisterMemberResponse(BaseModel):
    member: MemberResponse
    journal_entry_id: str
    journal_entry_hash: str

