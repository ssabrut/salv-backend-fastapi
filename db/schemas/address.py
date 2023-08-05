from pydantic import BaseModel
from datetime import datetime
from db.schemas import Response


class AddressBase(BaseModel):
    province: str
    city: str
    subdistrict: str
    ward: str
    address: str
    postal_code: str
    latitude: float
    longitude: float


class Address(AddressBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class AddressResponse(Response):
    data: list | Address | None = None
