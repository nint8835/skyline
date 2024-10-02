"""Create initial ContributionData model

Revision ID: 6a8e39e07452
Revises:
Create Date: 2024-10-02 16:43:07.593059

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6a8e39e07452"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contribution_data",
        sa.Column("user", sa.String(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column(
            "importer",
            sa.Enum("User", "Bot", name="contributionimporter", native_enum=False),
            nullable=False,
        ),
        sa.Column("contributions", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("user", "year", "importer"),
    )


def downgrade() -> None:
    op.drop_table("contribution_data")
