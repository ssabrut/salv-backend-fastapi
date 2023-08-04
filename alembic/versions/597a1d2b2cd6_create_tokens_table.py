"""create_token_table

Revision ID: 597a1d2b2cd6
Revises: 75c27be1f65f
Create Date: 2023-08-03 21:27:04.073379

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = "597a1d2b2cd6"
down_revision = "75c27be1f65f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tokens",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("token", sa.String(255), unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), default=func.now()),
    )


def downgrade() -> None:
    op.drop_column("tokens")
