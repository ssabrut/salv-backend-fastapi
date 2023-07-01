"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2023-07-01 13:02:00

"""

from alembic import op
from sqlalchemy import Column, String, Integer, Enum, Text, Float, DateTime
from sqlalchemy.sql import func
from db.enum import TypeEnum

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        Column("id", String(20), primary_key=True, unique=True, index=True),
        Column("type", Enum(TypeEnum)),
        Column("name", String(150), nullable=False, index=True),
        Column("username", String(50), nullable=False, unique=True),
        Column("password", String(150), nullable=False),
        Column("phone_number", String(15), nullable=False, index=True),
        Column("point", Integer, default=0, nullable=False, index=True),
        Column("province", String(50), nullable=False, index=True),
        Column("city", String(50), nullable=False, index=True),
        Column("subdistric", String(50), nullable=False, index=True),
        Column("ward", String(50), nullable=False, index=True),
        Column("address", Text, nullable=False, index=True),
        Column("postal_code", String(8), nullable=False, index=True),
        Column("image", String(255), default="", index=True),
        Column("latitude", Float, nullable=False, default=0, index=True),
        Column("longitude", Float, nullable=False, default=0, index=True),
        Column("created_at", DateTime(timezone=True), default=func.now()),
        Column("updated_at", DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table("users")
