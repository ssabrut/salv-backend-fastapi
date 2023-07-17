from pydantic import BaseModel
from datetime import datetime
from db.schemas import Response


class AdvertisementBase(BaseModel):
    food_waste_category_id: str
    user_id: str
    title: str
    location: str
    additional_information: str | None = ""
    price: int
    requested_weight: int
    minimum_weight: int
    maximum_weight: int


class Advertisement(AdvertisementBase):
    id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class AdvertisementResponse(Response):
    data: list | Advertisement | None = None
