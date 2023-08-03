"""create_addresses_table

Revision ID: 75c27be1f65f
Revises: e266a1857ce3
Create Date: 2023-08-03 15:32:00.605468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "75c27be1f65f"
down_revision = "e266a1857ce3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "addresses",
        sa.Column("user_id", sa.String(50)),
        sa.Column("province", sa.String(50), nullable=False, index=True),
        sa.Column("city", sa.String(50), nullable=False, index=True),
        sa.Column("subdistrict", sa.String(50), nullable=False, index=True),
        sa.Column("ward", sa.String(50), nullable=False, index=True),
        sa.Column("address", sa.Text, nullable=False, index=True),
        sa.Column("postal_code", sa.String(8), nullable=False, index=True),
        sa.Column("latitude", sa.Float, nullable=False, default=0, index=True),
        sa.Column("longitude", sa.Float, nullable=False, default=0, index=True),
    )
    op.create_foreign_key(
        "fk_addresses_user_id",
        "addresses",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_addresses_user_id", "addresses", type_="foreignkey")
    op.drop_table("addresses")
    op.drop_table("users")