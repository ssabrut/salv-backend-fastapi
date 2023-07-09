from sqlalchemy.orm import Session
from db.models import user as UserModel
import uuid
from decouple import config
import midtransclient


core_api = midtransclient.CoreApi(
    is_production=False,
    server_key=config("SERVER_KEY"),
    client_key=config("CLIENT_KEY"),
)


async def top_up(user_id: str, amount: int, db: Session):
    _uuid = "top-up-" + str(uuid.uuid4())
    user = db.query(UserModel.User).filter(UserModel.User.id == user_id).first()

    if user:
        param = {
            "payment_type": "gopay",
            "transaction_details": {
                "gross_amount": amount,
                "order_id": _uuid,
            },
            "customer_details": {
                "first_name": user.name.split()[0],
                "last_name": user.name.split()[-1],
                "phone": user.phone_number,
            },
        }

        charge_response = core_api.charge(param)
        return charge_response
    return "user not found"
