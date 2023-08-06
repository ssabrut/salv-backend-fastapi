from db.schemas import transaction as TransactionSchema
from fastapi import Depends, APIRouter, Request
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import transaction as TransactionCrud
import utils

router = APIRouter()


@router.get("/seller-transaction/index/{user_id}")
async def seller_transaction(
    user_id: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await TransactionCrud.index(db=db, token=token)
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
                    "message": "success get all transaction",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "no data", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/buyer-transaction/index/{user_id}")
async def buyer_transaction(
    user_id: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await TransactionCrud.index(db=db, token=token)
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
                    "message": "success get all transaction",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "no data", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.post("/seller-transaction")
async def create_transaction(
    transaction: TransactionSchema.TransactionBase,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        token = utils.get_token(request)
        data = await TransactionCrud.create(db=db, transaction=transaction, token=token)
        if utils.is_token_revoked(token, db):
            return jsonable_encoder(
                {
                    "status_code": 401,
                    "message": "token revoked",
                }
            )

        if data and type(data) != str:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "success to create transaction",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {
                "status_code": 400,
                "message": "failed to create transaction",
                "data": data,
            }
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/seller-transaction/{transaction_id}")
async def seller_transction(
    transaction_id: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await TransactionCrud.get(
            db=db, transaction_id=transaction_id, token=token
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
                    "message": "success getting transaction",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "failed getting transaction", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/buyer-transaction/{transaction_id}")
async def buyer_transction(
    transaction_id: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await TransactionCrud.get(
            db=db, transaction_id=transaction_id, token=token
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
                    "message": "success getting transaction",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "failed getting transaction", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/buyer-transaction/{transaction_id}/{status}")
async def update_transaction(
    transaction_id: str, status: int, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await TransactionCrud.update(
            db=db, transaction_id=transaction_id, status=status, token=token
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
                    "message": "success update transaction",
                }
            )
        return jsonable_encoder(
            {
                "status_code": 400,
                "message": "failed update transaction",
            }
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
