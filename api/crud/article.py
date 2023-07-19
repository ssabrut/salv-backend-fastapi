from sqlalchemy.orm import Session, joinedload
from db.models import article as ArticleModel
from db.schemas import article as ArticleSchema
from db.models import food_waste_category as CategoryModel
import uuid
import utils


async def index(db: Session, token: str):
    articles = (
        db.query(ArticleModel.Article)
        .join(
            CategoryModel.FoodWasteCategory,
            ArticleModel.Article.food_waste_category_id
            == CategoryModel.FoodWasteCategory.id,
        )
        .all()
    )
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        for i in range(len(articles)):
            articles[i] = {
                "user_id": articles[i].user_id,
                "category": articles[i].food_waste_category.name,
                "content": articles[i].content,
                "id": articles[i].id,
                "title": articles[i].title,
                "created_at": articles[i].created_at,
            }

        return articles
    return utils.credentials_exception


async def create(db: Session, article: ArticleSchema.ArticleBase, token: str):
    _uuid = str(uuid.uuid4())
    user = await utils.get_current_user(token=token, db=db)

    if user:
        data = {
            "id": _uuid,
            "user_id": user.id,
            "category": article.food_waste_category_id,
            "title": article.title,
            "content": article.content,
        }

        db_article = ArticleModel.Article(**data)
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article
    return utils.credentials_exception
