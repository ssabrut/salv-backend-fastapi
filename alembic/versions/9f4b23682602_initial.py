"""initial

Revision ID: 9f4b23682602
Revises: 
Create Date: 2023-07-01 13:55:20.289006

"""
from alembic import op
from sqlalchemy import Column, String, Integer, Text, DateTime, Date
from sqlalchemy.sql import func
from datetime import timedelta, date


# revision identifiers, used by Alembic.
revision = "9f4b23682602"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        Column("id", String(50), primary_key=True, unique=True, index=True),
        Column("type", Integer, nullable=False, index=True),
        Column("name", String(150), nullable=False, index=True),
        Column("username", String(50), nullable=False, unique=True),
        Column("password", String(150), nullable=False),
        Column("phone_number", String(15), nullable=False, index=True),
        Column("point", Integer, default=0, nullable=False, index=True),
        Column("image", String(255), default="", index=True),
        Column("created_at", DateTime(timezone=True), default=func.now()),
        Column("updated_at", DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "food_waste_categories",
        Column("id", String(50), primary_key=True, unique=True, index=True),
        Column("name", String(20), nullable=False, index=True),
        Column("created_at", DateTime(timezone=True), default=func.now()),
        Column("updated_at", DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "advertisements",
        Column("id", String(50), primary_key=True, unique=True, index=True),
        Column("food_waste_category_id", String(50)),
        Column("user_id", String(50)),
        Column("status", String(20), nullable=False, default="ongoing", index=True),
        Column("name", Text, nullable=False, index=True),
        Column("additional_information", Text, nullable=True, default="", index=True),
        Column("price", Integer, nullable=False, index=True),
        Column("requested_weight", Integer, nullable=False, index=True),
        Column("minimum_weight", Integer, nullable=False, index=True),
        Column("maximum_weight", Integer, nullable=False, index=True),
        Column("created_at", DateTime(timezone=True), default=func.now()),
        Column("updated_at", DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_advertisements_food_waste_category_id",
        "advertisements",
        "food_waste_categories",
        ["food_waste_category_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_advertisements_user_id",
        "advertisements",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_table(
        "educations",
        Column(
            "id", String(50), primary_key=True, unique=True, nullable=False, index=True
        ),
        Column("parent_id", String(50)),
        Column("food_waste_category_id", String(50)),
        Column("title", String(255), nullable=False, index=True),
        Column("content", Text, nullable=False),
        Column("duration", Integer, nullable=True, default=0),
        Column("video", String(255), nullable=True, default=""),
        Column("thumbnail", Text, nullable=False),
        Column("preparation", Text, nullable=False),
        Column("implementation", Text, nullable=False),
        Column("created_at", DateTime(timezone=True), default=func.now()),
        Column("updated_at", DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_educations_parent_id",
        "educations",
        "educations",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_table(
        "transactions",
        Column(
            "id", String(50), primary_key=True, unique=True, nullable=False, index=True
        ),
        Column("user_id", String(50)),
        Column("advertisement_id", String(50)),
        Column("status", String(10), nullable=True, default="pending"),
        Column("weight", Integer, nullable=False, index=True),
        Column("image", Text, nullable=False, index=True),
        Column("total_price", Integer, nullable=False, index=True),
        Column("created_at", DateTime(timezone=True), default=func.now()),
        Column("updated_at", DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_transactions_user_id",
        "transactions",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_transactions_advertisement_id",
        "transactions",
        "advertisements",
        ["advertisement_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_advertisements_food_waste_category_id", "advertisements", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_advertisements_user_id", "advertisements", type_="foreignkey"
    )
    op.drop_constraint("fk_transactions_user_id", "transactions", type_="foreignkey")
    op.drop_constraint(
        "fk_transactions_advertisement_id", "transactions", type_="foreignkey"
    )
    op.drop_table("transactions")
    op.drop_table("advertisements")
    op.drop_table("educations")
    op.drop_table("food_waste_categories")
    op.drop_table("users")