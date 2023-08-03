from db.engine import Base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func


class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, unique=True)
    token = Column(String(255), unique=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
