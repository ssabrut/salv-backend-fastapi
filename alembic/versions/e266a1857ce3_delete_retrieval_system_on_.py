"""delete_retrieval_system_on_advertisements_table

Revision ID: e266a1857ce3
Revises: cca235d91092
Create Date: 2023-07-16 12:33:57.935406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e266a1857ce3"
down_revision = "cca235d91092"
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass
    # op.drop_column("advertisements", "retrieval_system")


def downgrade() -> None:
    pass
