from db.schemas import advertisement as AdvertisementSchema
from fastapi import Depends, APIRouter, Request, Query
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import advertisement as AdvertisementCrud
from api.crud.user import is_address_exist
import utils

router = APIRouter()


@router.get("/check-address")
async def check_address(request: Request, db: Session = Depends(get_db)):
    try:
        token = utils.get_token(request)
        data = await is_address_exist(db=db, token=token)
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
                    "message": "success getting address",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "no address set", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/seller-advertisement/index")
async def seller_advertisement(request: Request, db: Session = Depends(get_db)):
    try:
        token = utils.get_token(request)
        data = await AdvertisementCrud.index(db=db, token=token)
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
                    "message": "success get all advertisement",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "no data", "data": data}
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
                    "message": "success get all advertisement",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "no data", "data": data}
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
                    "message": "success to create advertisement",
                }
            )
        return jsonable_encoder(
            {
                "status_code": 400,
                "message": "failed to create advertisement",
                "data": data,
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
                    "message": "advertisement found",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "advertisement not found", "data": data}
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
                    "message": "advertisement found",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "advertisement not found", "data": data}
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
                    "message": "advertisements found",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "no advertisements found", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/buyer-advertisement/cancel/{advertisement_id}")
async def cancel_advertisement(
    advertisement_id: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await AdvertisementCrud.cancel(
            advertisement_id=advertisement_id, db=db, token=token
        )

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
                    "message": "advertisements has been cancelled",
                }
            )
        return jsonable_encoder(
            {
                "status_code": 400,
                "message": "failed to cancel advertisement",
                "data": data,
            }
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/content-based/{categories}")
async def content_based(categories, request: Request, db: Session = Depends(get_db)):
    try:
        categories = [word.strip("''") for word in categories.strip("][").split(", ")]
        token = utils.get_token(request)
        data = await AdvertisementCrud.content_based(
            categories=categories, db=db, token=token
        )

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
                    "message": "success getting advertisement recommendation",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {
                "status_code": 400,
                "message": "failed getting advertisement recommendation",
                "data": data,
            }
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
