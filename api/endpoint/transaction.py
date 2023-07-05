from db.schemas import transaction as TransactionSchema
from fastapi import Depends, APIRouter
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import transaction as TransactionCrud

router = APIRouter()


@router.get("/transactions/user/{user_id}")
async def all_transaction(user_id: str, db: Session = Depends(get_db)):
    try:
        data = await TransactionCrud.index(db=db, user_id=user_id)

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
    transaction: TransactionSchema.TransactionBase, db: Session = Depends(get_db)
):
    try:
        data = await TransactionCrud.create(db=db, transaction=transaction)

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
