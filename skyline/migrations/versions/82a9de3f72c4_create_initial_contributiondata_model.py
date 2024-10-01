"""Create initial ContributionData model

Revision ID: 82a9de3f72c4
Revises:
Create Date: 2024-10-01 20:22:00.333838

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "82a9de3f72c4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contribution_data",
        sa.Column("user", sa.String(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("contributions", sa.String(), nullable=False),
        sa.Column(
            "importer",
            sa.Enum("User", "Bot", name="contributionimporter", native_enum=False),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("user", "year"),
    )


def downgrade() -> None:
    op.drop_table("contribution_data")
