"""create sortition tables

Revision ID: 20260514_0002
Revises: 20260513_0001
Create Date: 2026-05-14
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260514_0002"
down_revision: str | None = "20260513_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "eligibility_pools",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("arena_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("pool_hash", sa.String(length=71), nullable=False),
        sa.Column("member_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "eligibility_pool_members",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("pool_id", sa.String(length=36), nullable=False),
        sa.Column("member_id", sa.String(length=36), nullable=False),
        sa.Column("public_identity_id", sa.String(length=36), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"]),
        sa.ForeignKeyConstraint(["pool_id"], ["eligibility_pools.id"]),
        sa.ForeignKeyConstraint(["public_identity_id"], ["public_identities.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pool_id", "member_id", name="uq_eligibility_pool_member"),
    )
    op.create_table(
        "sortition_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("pool_id", sa.String(length=36), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("target_seats", sa.Integer(), nullable=False),
        sa.Column("reserve_seats", sa.Integer(), nullable=False),
        sa.Column("seed", sa.String(length=160), nullable=False),
        sa.Column("algorithm", sa.String(length=80), nullable=False),
        sa.Column("transcript_hash", sa.String(length=71), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["pool_id"], ["eligibility_pools.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sortition_results",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("member_id", sa.String(length=36), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("seat_type", sa.String(length=32), nullable=False),
        sa.Column("selection_hash", sa.String(length=71), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"]),
        sa.ForeignKeyConstraint(["run_id"], ["sortition_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("run_id", "member_id", name="uq_sortition_result_member"),
        sa.UniqueConstraint("run_id", "rank", name="uq_sortition_result_rank"),
    )


def downgrade() -> None:
    op.drop_table("sortition_results")
    op.drop_table("sortition_runs")
    op.drop_table("eligibility_pool_members")
    op.drop_table("eligibility_pools")
