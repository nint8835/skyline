"""Create initial ContributionData model

Revision ID: 7456e404c50c
Revises:
Create Date: 2024-10-01 18:20:25.185638

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7456e404c50c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contribution_data",
        sa.Column("user", sa.String(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("contributions", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("user", "year"),
    )


def downgrade() -> None:
    op.drop_table("contribution_data")
