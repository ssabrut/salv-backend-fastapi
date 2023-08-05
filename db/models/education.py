from db.engine import Base
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Education(Base):
    __tablename__ = "educations"
    id = Column(String(50), primary_key=True, unique=True)
    parent_id = Column(String(50), ForeignKey("educations.id"), nullable=True)
    food_waste_category_id = Column(String(50), ForeignKey("food_waste_categories.id"))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    duration = Column(Integer, nullable=True, default=0)
    video = Column(Text, nullable=True, default="")
    thumbnail = Column(Text, nullable=False)
    preparation = Column(Text, nullable=False)
    implementation = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Establishing relationships
    parent = relationship(
        "Education",
        remote_side=[id],
        backref="educations",
        primaryjoin="Education.parent_id == Education.id",
    )
    food_waste_category = relationship("FoodWasteCategory", backref="educations")
