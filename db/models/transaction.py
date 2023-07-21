from db.engine import Base
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String(50), primary_key=True, unique=True)
    user_id = Column(String(50), ForeignKey("users.id"))
    advertisement_id = Column(String(50), ForeignKey("advertisements.id"))
    status = Column(Integer, nullable=True, default=0)
    weight = Column(Integer, nullable=False, index=True)
    location = Column(Text, nullable=False, index=True)
    image = Column(String(255), nullable=False, index=True)
    total_price = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Establishing relationships
    user = relationship("User", backref="transactions")
    advertisement = relationship("Advertisement", backref="transactions")
