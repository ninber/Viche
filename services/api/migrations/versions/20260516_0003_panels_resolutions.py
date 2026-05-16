"""Add panels, mandates, and resolutions.

Revision ID: 20260516_0003
Revises: 20260514_0002
Create Date: 2026-05-16 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260516_0003"
down_revision: str | None = "20260514_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "panels",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("proposal_id", sa.String(length=36), nullable=False),
        sa.Column("sortition_run_id", sa.String(length=36), nullable=False),
        sa.Column("arena_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("mandate_summary", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["proposal_id"], ["proposals.id"]),
        sa.ForeignKeyConstraint(["sortition_run_id"], ["sortition_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sortition_run_id"),
    )
    op.create_table(
        "panel_mandates",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("panel_id", sa.String(length=36), nullable=False),
        sa.Column("member_id", sa.String(length=36), nullable=False),
        sa.Column("sortition_result_id", sa.String(length=36), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"]),
        sa.ForeignKeyConstraint(["panel_id"], ["panels.id"]),
        sa.ForeignKeyConstraint(["sortition_result_id"], ["sortition_results.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("panel_id", "member_id", name="uq_panel_mandate_member"),
    )
    op.create_table(
        "resolutions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("panel_id", sa.String(length=36), nullable=False),
        sa.Column("proposal_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("body_markdown", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("decision_method", sa.String(length=80), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["panel_id"], ["panels.id"]),
        sa.ForeignKeyConstraint(["proposal_id"], ["proposals.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("resolutions")
    op.drop_table("panel_mandates")
    op.drop_table("panels")
