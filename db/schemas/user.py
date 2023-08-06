from pydantic import BaseModel
from datetime import datetime
from db.schemas import Response


class UserBase(BaseModel):
    type: int
    name: str
    username: str
    email: str
    phone_number: str
    point: int | None = 0
    image: str | None = ""


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class UserResponse(Response):
    token: str
    token_type: str
    data: str | User | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class AddressBase(BaseModel):
    province: str
    city: str
    subdistrict: str
    ward: str
    address: str
    postal_code: str
    latitude: float | None = 0.0
    longitude: float | None = 0.0


class Address(AddressBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
