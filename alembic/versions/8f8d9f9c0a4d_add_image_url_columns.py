"""
Add image_url columns to meals and articles if missing

Revision ID: 8f8d9f9c0a4d
Revises: c3a3f7091608
Create Date: 2025-08-09 14:25:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8f8d9f9c0a4d"
down_revision = "c3a3f7091608"
branch_labels = None
depends_on = None


def _has_column(inspector: sa.engine.reflection.Inspector, table: str, column: str) -> bool:
    try:
        cols = inspector.get_columns(table)
    except Exception:
        return False
    return any(c.get("name") == column for c in cols)


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)

    if not _has_column(insp, "meals", "image_url"):
        op.add_column("meals", sa.Column("image_url", sa.String(length=1024), nullable=True))

    if not _has_column(insp, "articles", "image_url"):
        op.add_column("articles", sa.Column("image_url", sa.String(length=1024), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)

    if _has_column(insp, "meals", "image_url"):
        op.drop_column("meals", "image_url")

    if _has_column(insp, "articles", "image_url"):
        op.drop_column("articles", "image_url")


