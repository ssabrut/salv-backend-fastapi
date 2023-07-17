from pydantic import BaseModel
from datetime import datetime
from db.schemas import Response


class FoodWasteCategoryBase(BaseModel):
    name: str


class FoodWasteCategory(FoodWasteCategoryBase):
    id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class FoodWasteCategoryResponse(Response):
    data: list | FoodWasteCategory | None = None
