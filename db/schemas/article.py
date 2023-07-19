from pydantic import BaseModel
from datetime import datetime
from db.schemas import Response


class ArticleBase(BaseModel):
    food_waste_category_id: str
    title: str
    content: str


class Article(ArticleBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class ArticleResponse(Response):
    data: list | Article | None = None
