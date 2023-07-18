from db.schemas import advertisement as AdvertisementSchema
from fastapi import Depends, APIRouter, Request
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import advertisement as AdvertisementCrud
import utils

router = APIRouter()


@router.get("/advertisements/user/{user_id}")
async def all_advertisement(
    user_id: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await AdvertisementCrud.index(db=db, user_id=user_id, token=token)

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "success get all advertisement",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "failed get all advertisement"}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.post(
    "/advertisements/create", response_model=AdvertisementSchema.AdvertisementResponse
)
async def create_advertisement(
    advertisement: AdvertisementSchema.AdvertisementBase,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        token = utils.get_token(request)
        data = await AdvertisementCrud.create(
            db=db, advertisement=advertisement, token=token
        )

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "success to create advertisement",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {
                "status_code": 400,
                "message": "failed to create advertisement",
            }
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/advertisements/{advertisement_id}")
async def get_advertisement(
    advertisement_id: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await AdvertisementCrud.get(
            db=db, advertisement_id=advertisement_id, token=token
        )

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "advertisement found",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {
                "status_code": 400,
                "message": "advertisement not found",
            }
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/advertisements/search/{query}")
async def search_advertisement(
    query: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await AdvertisementCrud.search(db=db, query=query, token=token)

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "advertisements found",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {
                "status_code": 400,
                "message": "no advertisements found",
            }
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
