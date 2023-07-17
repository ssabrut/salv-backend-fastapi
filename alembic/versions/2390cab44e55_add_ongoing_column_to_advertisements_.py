"""add ongoing column to advertisements table

Revision ID: 2390cab44e55
Revises: 9f4b23682602
Create Date: 2023-07-04 13:50:50.041189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2390cab44e55"
down_revision = "9f4b23682602"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "advertisements",
        sa.Column("ongoing_weight", sa.Integer, nullable=True, default=0, index=True),
    )


def downgrade() -> None:
    op.drop_column("advertisements", "ongoing_weight")
