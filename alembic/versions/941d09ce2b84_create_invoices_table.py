"""create invoices table

Revision ID: 941d09ce2b84
Revises: bdfe0e8791a4
Create Date: 2023-07-09 19:08:41.637808

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = "941d09ce2b84"
down_revision = "bdfe0e8791a4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "invoices",
        sa.Column("id", sa.String(50), primary_key=True, unique=True, index=True),
        sa.Column("user_id", sa.String(50)),
        sa.Column("order_id", sa.String(50), index=True),
        sa.Column("amount", sa.Integer),
        sa.Column("created_at", sa.DateTime(timezone=True), default=func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_invoices_user_id",
        "invoices",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_invoices_user_id", "invoices", type_="foreignkey")
    op.drop_table("invoices")
