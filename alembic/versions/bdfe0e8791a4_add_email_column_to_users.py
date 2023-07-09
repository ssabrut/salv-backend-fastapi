"""add email column to users

Revision ID: bdfe0e8791a4
Revises: 2390cab44e55
Create Date: 2023-07-09 15:47:19.051875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bdfe0e8791a4"
down_revision = "2390cab44e55"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("email", sa.String(100), nullable=False, index=True),
    )


def downgrade() -> None:
    op.drop_column("users", "email")
