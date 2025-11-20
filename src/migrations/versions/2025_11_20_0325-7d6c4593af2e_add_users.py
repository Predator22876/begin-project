"""add users

Revision ID: 7d6c4593af2e
Revises: cf7d37b6c5f5
Create Date: 2025-11-20 03:25:02.192647

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7d6c4593af2e"
down_revision: Union[str, Sequence[str], None] = "cf7d37b6c5f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
