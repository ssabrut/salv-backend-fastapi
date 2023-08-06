from db.engine import Base
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func


class FoodWasteCategory(Base):
    __tablename__ = "food_waste_categories"
    id = Column(String(50), primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    image = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
