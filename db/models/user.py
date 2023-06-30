from engine import Base
from sqlalchemy import Column, String, Integer, Enum, Text, Float, DateTime
from sqlalchemy.sql import func
from db.enum import TypeEnum


class User(Base):
    __tablename__ = "users"
    id = Column(String(20), primary_key=True, unique=True, index=True)
    type = Column(Enum(TypeEnum))
    name = Column(String(150), nullable=False, index=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    phone_number = Column(String(15), nullable=False, index=True)
    point = Column(Integer, default=0, nullable=False, index=True)
    province = Column(String(50), nullable=False, index=True)
    city = Column(String(50), nullable=False, index=True)
    subdistrict = Column(String(50), nullable=False, index=True)
    ward = Column(String(50), nullable=False, index=True)
    address = Column(Text, nullable=False, index=True)
    postal_code = Column(String(8), nullable=False, index=True)
    image = Column(String(255), default="", index=True)
    latitude = Column(Float, nullable=False, default=0, index=True)
    longitude = Column(Float, nullable=False, default=0, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
