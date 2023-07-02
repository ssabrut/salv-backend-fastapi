from pydantic import BaseModel, validator
from sqlalchemy import DateTime
from datetime import datetime


class UserBase(BaseModel):
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
    id: str
    created_at: datetime
    updated_at: datetime | None = None

    @validator("created_at", "updated_at", pre=True)
    def validate_datetime(cls, value):
        if isinstance(value, DateTime):
            # Convert the value to a Python datetime object
            value = value.datetime
        return value

    class Config:
        orm_mode = True
