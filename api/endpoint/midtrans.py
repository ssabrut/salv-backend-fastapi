from fastapi import Depends, APIRouter, Request
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import midtrans as MidTransCrud
import utils


router = APIRouter()


@router.get("/midtrans/top-up/{amount}")
async def top_up(amount: int, request: Request, db: Session = Depends(get_db)):
    try:
        token = utils.get_token(request)
        data = await MidTransCrud.top_up(amount=amount, db=db, token=token)
        if utils.is_token_revoked(token, db):
            return jsonable_encoder(
                {
                    "status_code": 401,
                    "message": "token revoked",
                }
            )

        if type(data) is not str and data:
            return jsonable_encoder(data)
        return jsonable_encoder(
            {"status_code": 400, "message": "register failed", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/midtrans/success/{transaction_id}")
async def success(transaction_id: str, request: Request, db: Session = Depends(get_db)):
    try:
        token = utils.get_token(request)
        data = await MidTransCrud.add_point(
            transaction_id=transaction_id, db=db, token=token
        )

        if utils.is_token_revoked(token, db):
            return jsonable_encoder(
                {
                    "status_code": 401,
                    "message": "token revoked",
                }
            )

        if type(data) is not str and data:
            return jsonable_encoder(
                {"status_code": 200, "message": "success adding point"}
            )
        return jsonable_encoder({"status_code": 400, "message": "failed adding point"})
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


# @router.post("/midtrans/cancel/{order_id}")
# async def cancel(order_id: str, request: Request):
#     try:
#         token = utils.get_token(request)
#         await MidTransCrud.cancel(order_id=order_id)
#     except Exception as e:
#         return jsonable_encoder({"status_code": 500, "message": str(e)})
