from db.engine import Base
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(String(50), primary_key=True, unique=True)
    user_id = Column(String(50), ForeignKey("users.id"))
    order_id = Column(String(50), nullable=False, index=True)
    amount = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Establishing relationships
    user = relationship("User", backref="invoices")
