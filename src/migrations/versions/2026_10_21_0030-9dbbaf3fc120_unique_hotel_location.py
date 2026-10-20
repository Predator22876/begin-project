"""make hotel location unique

Revision ID: 9dbbaf3fc120
Revises: 3853881c7c4a
Create Date: 2026-10-21

"""

from typing import Sequence, Union

from alembic import op


revision: str = "9dbbaf3fc120"
down_revision: Union[str, Sequence[str], None] = "3853881c7c4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_hotels_location", "hotels", ["location"])


def downgrade() -> None:
    op.drop_constraint("uq_hotels_location", "hotels", type_="unique")
