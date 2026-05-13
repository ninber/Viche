from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ConsentRecord, Member, PublicIdentity
from app.db.session import get_db
from app.domain.journal import append_journal_entry
from app.schemas.members import (
    MemberResponse,
    PublicIdentityResponse,
    RegisterMemberRequest,
    RegisterMemberResponse,
)

router = APIRouter()
DbSession = Annotated[AsyncSession, Depends(get_db)]


def _public_handle(member_id: str) -> str:
    return f"member-{member_id[:8]}"


def _member_response(member: Member, public_identity: PublicIdentity) -> MemberResponse:
    return MemberResponse(
        id=member.id,
        display_locale=member.display_locale,
        assurance_level=member.assurance_level,
        status=member.status,
        public_identity=PublicIdentityResponse(
            id=public_identity.id,
            handle=public_identity.handle,
            display_name=public_identity.display_name,
        ),
        created_at=member.created_at,
    )


@router.post(
    "/members/register",
    response_model=RegisterMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_member(
    request: RegisterMemberRequest,
    session: DbSession,
) -> RegisterMemberResponse:
    member = Member(
        display_locale=request.display_locale,
        assurance_level=request.assurance_method,
    )
    session.add(member)
    await session.flush()

    public_identity = PublicIdentity(
        member_id=member.id,
        handle=_public_handle(member.id),
        display_name=request.public_display_name,
    )
    consent = ConsentRecord(
        member_id=member.id,
        privacy_notice_version=request.consents.privacy_notice_version,
        terms_version=request.consents.terms_version,
        public_profile_opt_in=request.consents.public_profile_opt_in,
    )
    session.add_all([public_identity, consent])
    await session.flush()

    journal = await append_journal_entry(
        session,
        event_type="member.registered",
        actor_type="system",
        actor_id=None,
        subject_type="member",
        subject_id=member.id,
        payload={
            "member_id": member.id,
            "public_identity_id": public_identity.id,
            "display_locale": member.display_locale,
            "assurance_level": member.assurance_level,
            "privacy_notice_version": consent.privacy_notice_version,
            "terms_version": consent.terms_version,
        },
    )
    await session.commit()

    return RegisterMemberResponse(
        member=_member_response(member, public_identity),
        journal_entry_id=journal.id,
        journal_entry_hash=journal.entry_hash,
    )


@router.get("/members/{member_id}", response_model=MemberResponse)
async def get_member(
    member_id: str,
    session: DbSession,
) -> MemberResponse:
    member = await session.get(Member, member_id)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="member not found")
    await session.refresh(member, attribute_names=["public_identity"])
    return _member_response(member, member.public_identity)
