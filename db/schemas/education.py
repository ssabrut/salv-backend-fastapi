from pydantic import BaseModel
from datetime import datetime
from db.schemas import Response


class EducationBase(BaseModel):
    parent_id: str | None = None
    food_waste_category_id: str
    title: str
    content: str
    duration: int | None = 0
    video: str | None = ""
    thumbnail: str
    preparation: str
    implementation: str


class Education(EducationBase):
    id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class EducationResponse(Response):
    data: list | Education | None = None
