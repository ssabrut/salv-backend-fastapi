from db.schemas import article as ArticleSchema
from api.crud import article as ArticleCrud
from fastapi import Depends, APIRouter, Request
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
import utils

router = APIRouter()


@router.get("/articles")
async def all_article(request: Request, db: Session = Depends(get_db)):
    try:
        token = utils.get_token(request)
        data = await ArticleCrud.index(db=db, token=token)

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "success get all article",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "failed get all article"}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.post("/articles/create")
async def create_article(
    article: ArticleSchema.ArticleBase, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await ArticleCrud.create(db=db, article=article, token=token)

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "success create article",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "failed create article"}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
