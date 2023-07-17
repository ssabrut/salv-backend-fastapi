"""create_articles_table

Revision ID: cca235d91092
Revises: 8f7d6992ad74
Create Date: 2023-07-15 14:52:49.331761

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = "cca235d91092"
down_revision = "8f7d6992ad74"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "articles",
        sa.Column(
            "id",
            sa.String(50),
            primary_key=True,
            unique=True,
            nullable=False,
            index=True,
        ),
        sa.Column("user_id", sa.String(50)),
        sa.Column("food_waste_category_id", sa.String(50)),
        sa.Column("title", sa.String(255), nullable=False, index=True),
        sa.Column("content", sa.Text, nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), default=func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_articles_user_id",
        "articles",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_articles_food_waste_category_id",
        "articles",
        "food_waste_categories",
        ["food_waste_category_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_table("articles")
