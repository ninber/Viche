from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, new_uuid


class Member(TimestampMixin, Base):
    __tablename__ = "members"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    display_locale: Mapped[str] = mapped_column(String(16), nullable=False, default="uk-UA")
    assurance_level: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="self_declared",
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")

    public_identity: Mapped["PublicIdentity"] = relationship(back_populates="member")
    consents: Mapped[list["ConsentRecord"]] = relationship(back_populates="member")
    proposals: Mapped[list["Proposal"]] = relationship(back_populates="submitter")


class PublicIdentity(TimestampMixin, Base):
    __tablename__ = "public_identities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), nullable=False, unique=True)
    handle: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    display_name: Mapped[str | None] = mapped_column(String(160), nullable=True)

    member: Mapped[Member] = relationship(back_populates="public_identity")


class ConsentRecord(TimestampMixin, Base):
    __tablename__ = "consent_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), nullable=False)
    privacy_notice_version: Mapped[str] = mapped_column(String(64), nullable=False)
    terms_version: Mapped[str] = mapped_column(String(64), nullable=False)
    public_profile_opt_in: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    member: Mapped[Member] = relationship(back_populates="consents")


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    sequence: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id: Mapped[str] = mapped_column(String(36), default=new_uuid, nullable=False, unique=True)
    event_type: Mapped[str] = mapped_column(String(120), nullable=False)
    actor_type: Mapped[str] = mapped_column(String(80), nullable=False)
    actor_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    subject_type: Mapped[str] = mapped_column(String(80), nullable=False)
    subject_id: Mapped[str] = mapped_column(String(120), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    payload_hash: Mapped[str] = mapped_column(String(71), nullable=False)
    previous_hash: Mapped[str | None] = mapped_column(String(71), nullable=True)
    entry_hash: Mapped[str] = mapped_column(String(71), nullable=False, unique=True)
    occurred_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)


class Proposal(TimestampMixin, Base):
    __tablename__ = "proposals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    submitter_member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), nullable=False)
    arena_id: Mapped[str] = mapped_column(String(36), nullable=False)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    body_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False, default="UA")
    region_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    district_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    community_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="submitted")
    tags: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)

    submitter: Mapped[Member] = relationship(back_populates="proposals")
    outgoing_relations: Mapped[list["ProposalRelation"]] = relationship(
        back_populates="source",
        foreign_keys="ProposalRelation.source_proposal_id",
    )


class ProposalRelation(TimestampMixin, Base):
    __tablename__ = "proposal_relations"
    __table_args__ = (
        UniqueConstraint(
            "source_proposal_id",
            "target_proposal_id",
            "relation_type",
            name="uq_proposal_relation_edge",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    source_proposal_id: Mapped[str] = mapped_column(ForeignKey("proposals.id"), nullable=False)
    target_proposal_id: Mapped[str] = mapped_column(ForeignKey("proposals.id"), nullable=False)
    relation_type: Mapped[str] = mapped_column(String(64), nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)

    source: Mapped[Proposal] = relationship(
        back_populates="outgoing_relations",
        foreign_keys=[source_proposal_id],
    )


class EligibilityPool(TimestampMixin, Base):
    __tablename__ = "eligibility_pools"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    arena_id: Mapped[str] = mapped_column(String(36), nullable=False)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="frozen")
    pool_hash: Mapped[str] = mapped_column(String(71), nullable=False)
    member_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    members: Mapped[list["EligibilityPoolMember"]] = relationship(back_populates="pool")
    sortition_runs: Mapped[list["SortitionRun"]] = relationship(back_populates="pool")


class EligibilityPoolMember(Base):
    __tablename__ = "eligibility_pool_members"
    __table_args__ = (
        UniqueConstraint("pool_id", "member_id", name="uq_eligibility_pool_member"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    pool_id: Mapped[str] = mapped_column(ForeignKey("eligibility_pools.id"), nullable=False)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), nullable=False)
    public_identity_id: Mapped[str] = mapped_column(
        ForeignKey("public_identities.id"),
        nullable=False,
    )
    weight: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    pool: Mapped[EligibilityPool] = relationship(back_populates="members")


class SortitionRun(TimestampMixin, Base):
    __tablename__ = "sortition_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    pool_id: Mapped[str] = mapped_column(ForeignKey("eligibility_pools.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="completed")
    target_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    reserve_seats: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    seed: Mapped[str] = mapped_column(String(160), nullable=False)
    algorithm: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        default="sha256_member_order_v1",
    )
    transcript_hash: Mapped[str] = mapped_column(String(71), nullable=False)

    pool: Mapped[EligibilityPool] = relationship(back_populates="sortition_runs")
    results: Mapped[list["SortitionResult"]] = relationship(back_populates="run")


class SortitionResult(Base):
    __tablename__ = "sortition_results"
    __table_args__ = (
        UniqueConstraint("run_id", "member_id", name="uq_sortition_result_member"),
        UniqueConstraint("run_id", "rank", name="uq_sortition_result_rank"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    run_id: Mapped[str] = mapped_column(ForeignKey("sortition_runs.id"), nullable=False)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    seat_type: Mapped[str] = mapped_column(String(32), nullable=False)
    selection_hash: Mapped[str] = mapped_column(String(71), nullable=False)

    run: Mapped[SortitionRun] = relationship(back_populates="results")
