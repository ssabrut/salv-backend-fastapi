from db.schemas import transaction as TransactionSchema
from fastapi import Depends, APIRouter, Request
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import transaction as TransactionCrud

router = APIRouter()


@router.get("/transactions/user/{user_id}")
async def all_transaction(
    user_id: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = request.headers["authorization"].split()[-1]
        data = await TransactionCrud.index(db=db, user_id=user_id, token=token)

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "success get all transaction",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "failed get all transaction"}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.post(
    "/transactions/create", response_model=TransactionSchema.TransactionResponse
)
async def create_transaction(
    transaction: TransactionSchema.TransactionBase,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        token = request.headers["authorization"].split()[-1]
        data = await TransactionCrud.create(db=db, transaction=transaction, token=token)

        if data:
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
            }
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.get("/transactions/{transaction_id}")
async def get_transction(
    transaction_id: str, request: Request, db: Session = Depends(get_db)
):
    try:
        token = request.headers["authorization"].split()[-1]
        data = await TransactionCrud.get(
            db=db, transaction_id=transaction_id, token=token
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
            {
                "status_code": 400,
                "message": "failed getting transaction",
            }
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
