from fastapi import Depends, APIRouter
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import midtrans as MidTransCrud


router = APIRouter()


@router.get("/midtrans/top-up/{user_id}/{amount}")
async def top_up(user_id: str, amount: int, db: Session = Depends(get_db)):
    try:
        data = await MidTransCrud.top_up(user_id=user_id, amount=amount, db=db)

        if type(data) is not str and data:
            return jsonable_encoder(data)
        return jsonable_encoder(
            {"status_code": 400, "message": "register failed", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


# @router.get("/midtrans/test")
# async def test():
#     param = {
#         "payment_type": "gopay",
#         "transaction_details": {
#             "gross_amount": 12145,
#             "order_id": "test-transaction-542321",
#         },
#         "gopay": {
#             "enable_callback": True,  # optional
#             "callback_url": "someapps://callback",  # optional
#         },
#         "customer_details": {
#             "first_name": "Anna",
#         },
#     }

#     # charge transaction
#     charge_response = core_api.charge(param)
#     return jsonable_encoder({"data": charge_response})
