from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    id: str
    type: int
    name: str
    username: str
    phone_number: str
    province: str
    city: str
    subdistrict: str
    ward: str
    address: str
    postal_code: str
    point: int | None = 0
    image: str | None = ""
    latitude: float | None = 0.0
    longitude: float | None = 0.0


class UserCreate(UserBase):
    password: str


class User(UserBase):
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
