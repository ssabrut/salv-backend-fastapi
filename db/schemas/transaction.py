from pydantic import BaseModel
from datetime import datetime
from db.schemas import Response


class TransactionBase(BaseModel):
    user_id: str
    advertisement_id: str
    retrieval_system: int
    weight: int
    location: str
    image: str
    total_price: int


class Transaction(TransactionBase):
    id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class TransactionResponse(Response):
    data: list | Transaction | None = None
