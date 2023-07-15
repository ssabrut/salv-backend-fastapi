from db.engine import Base
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Article(Base):
    __tablename__ = "articles"
    id = Column(String(50), primary_key=True, unique=True)
    user_id = Column(String(50), ForeignKey("users.id"))
    food_waste_category_id = Column(String(50), ForeignKey("food_waste_categories.id"))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Establishing relationships
    user = relationship("User", backref="articles")
    food_waste_category = relationship("FoodWasteCategory", backref="articles")
  