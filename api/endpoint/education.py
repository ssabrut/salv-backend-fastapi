from fastapi import Depends, APIRouter, Request
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import education
import utils

router = APIRouter()


@router.get("/education/index")
async def index(request: Request, db: Session = Depends(get_db)):
    try:
        token = utils.get_token(request)
        data = await education.index(db=db, token=token)
        if utils.is_token_revoked(token, db):
            return jsonable_encoder(
                {
                    "status_code": 401,
                    "message": "token revoked",
                }
            )

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "success fetch all education",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "failed fetch all education"}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/education/{education_id}")
async def get_education(
    request: Request, education_id: str, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await education.get(education_id=education_id, db=db, token=token)
        if utils.is_token_revoked(token, db):
            return jsonable_encoder(
                {
                    "status_code": 401,
                    "message": "token revoked",
                }
            )

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "success fetch education",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "failed fetch education"}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
