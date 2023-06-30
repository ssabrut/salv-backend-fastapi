from pydantic import BaseModel
from sqlalchemy import DateTime


class UserBase(BaseModel):
    name: str
    username: str
    phone_number: str
    province: str
    city: str
    subdistrict: str
    ward: str
    address: str
    postal_code: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    type: int
    point: int | None = 0
    image: str | None = ""
    latitude: float | None = 0.0
    longitude: float | None = 0.0
    created_at: DateTime
    updated_at: DateTime | None = None

    class Config:
        orm_mode = True
