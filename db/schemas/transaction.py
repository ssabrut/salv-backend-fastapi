from pydantic import BaseModel
from datetime import datetime
from db.schemas import Response


class TransactionBase(BaseModel):
    advertisement_id: str
    weight: int
    location: str
    image: str


class Transaction(TransactionBase):
    id: str
    user_id: str
    total_price: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class TransactionResponse(Response):
    data: str | list | Transaction | None = None
