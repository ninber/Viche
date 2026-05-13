"""create core civic tables

Revision ID: 20260513_0001
Revises:
Create Date: 2026-05-13
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260513_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "members",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("display_locale", sa.String(length=16), nullable=False),
        sa.Column("assurance_level", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "journal_entries",
        sa.Column("sequence", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("actor_type", sa.String(length=80), nullable=False),
        sa.Column("actor_id", sa.String(length=120), nullable=True),
        sa.Column("subject_type", sa.String(length=80), nullable=False),
        sa.Column("subject_id", sa.String(length=120), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("payload_hash", sa.String(length=71), nullable=False),
        sa.Column("previous_hash", sa.String(length=71), nullable=True),
        sa.Column("entry_hash", sa.String(length=71), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("sequence"),
        sa.UniqueConstraint("entry_hash"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "consent_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("member_id", sa.String(length=36), nullable=False),
        sa.Column("privacy_notice_version", sa.String(length=64), nullable=False),
        sa.Column("terms_version", sa.String(length=64), nullable=False),
        sa.Column("public_profile_opt_in", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "public_identities",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("member_id", sa.String(length=36), nullable=False),
        sa.Column("handle", sa.String(length=80), nullable=False),
        sa.Column("display_name", sa.String(length=160), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("handle"),
        sa.UniqueConstraint("member_id"),
    )
    op.create_table(
        "proposals",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("submitter_member_id", sa.String(length=36), nullable=False),
        sa.Column("arena_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("body_markdown", sa.Text(), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("region_code", sa.String(length=32), nullable=True),
        sa.Column("district_code", sa.String(length=32), nullable=True),
        sa.Column("community_code", sa.String(length=32), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["submitter_member_id"], ["members.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "proposal_relations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_proposal_id", sa.String(length=36), nullable=False),
        sa.Column("target_proposal_id", sa.String(length=36), nullable=False),
        sa.Column("relation_type", sa.String(length=64), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["source_proposal_id"], ["proposals.id"]),
        sa.ForeignKeyConstraint(["target_proposal_id"], ["proposals.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "source_proposal_id",
            "target_proposal_id",
            "relation_type",
            name="uq_proposal_relation_edge",
        ),
    )
    op.create_index("ix_proposals_status_created_at", "proposals", ["status", "created_at"])
    op.create_index("ix_journal_entries_event_type", "journal_entries", ["event_type"])


def downgrade() -> None:
    op.drop_index("ix_journal_entries_event_type", table_name="journal_entries")
    op.drop_index("ix_proposals_status_created_at", table_name="proposals")
    op.drop_table("proposal_relations")
    op.drop_table("proposals")
    op.drop_table("public_identities")
    op.drop_table("consent_records")
    op.drop_table("journal_entries")
    op.drop_table("members")

