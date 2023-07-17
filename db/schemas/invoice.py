from pydantic import BaseModel
from datetime import datetime
from db.schemas import Response


class InvoiceBase(BaseModel):
    user_id: str
    order_id: str
    amount: int
    status: str


class Invoice(InvoiceBase):
    id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class InvoiceResponse(Response):
    data: str | list | Invoice | None = None
