from db.schemas import advertisement as AdvertisementSchema
from fastapi import Depends, APIRouter, Request
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import advertisement as AdvertisementCrud
import utils

router = APIRouter()


@router.get("/seller-advertisement/index")
async def seller_advertisement(request: Request, db: Session = Depends(get_db)):
    try:
        token = utils.get_token(request)
        data = await AdvertisementCrud.index(db=db, token=token)

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


@router.get("/buyer-advertisement/index/{user_id}")
async def buyer_advertisement(
    user_id: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await AdvertisementCrud.index(db=db, token=token)

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


@router.post("/buyer-advertisement")
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


@router.get("/seller-advertisement/{advertisement_id}")
async def seller_advertisement(
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


@router.get("/buyer-advertisement/{advertisement_id}")
async def buyer_advertisement(
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


@router.get("/seller-advertisement/search/{query}")
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
