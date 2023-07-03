from pydantic import BaseModel
from datetime import datetime


class AdvertisementBase(BaseModel):
    status: str
    title: str
    retrieval_system: int
    location: str
    additional_information: str | None = ""
    price: int
    requested_weight: int
    minimum_weight: int
    maximum_weight: int


class Advertisement(AdvertisementBase):
    id: str
    food_waste_category_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
