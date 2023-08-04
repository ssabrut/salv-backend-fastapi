from db.engine import Base
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Advertisement(Base):
    __tablename__ = "advertisements"
    id = Column(String(50), primary_key=True, unique=True)
    food_waste_category_id = Column(String(50), ForeignKey("food_waste_categories.id"))
    user_id = Column(String(50), ForeignKey("users.id"))
    status = Column(String(50), nullable=False, default="ongoing")
    name = Column(String(255), nullable=False)
    additional_information = Column(Text, nullable=True, default="")
    price = Column(Integer, nullable=False)
    ongoing_weight = Column(Integer, nullable=True, default=0)
    requested_weight = Column(Integer, nullable=False)
    minimum_weight = Column(Integer, nullable=False)
    maximum_weight = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Establishing relationships
    food_waste_category = relationship("FoodWasteCategory", backref="advertisements")
    user = relationship("User", backref="advertisements")
