from pydantic import BaseModel
from datetime import datetime


class FoodWasteCategoryBase(BaseModel):
    name: str


class FoodWasteCategory(FoodWasteCategoryBase):
    id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class FoodWasteCategoryResponse(BaseModel):
    status_code: int
    message: str
    data: list(FoodWasteCategory) | None = None
