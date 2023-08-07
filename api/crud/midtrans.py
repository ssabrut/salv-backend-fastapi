from sqlalchemy.orm import Session
from db.models import user as UserModel
import uuid
import os
import midtransclient
from api.crud import invoice as InvoiceCrud
from dotenv import load_dotenv
import utils

load_dotenv()


core_api = midtransclient.CoreApi(
    is_production=False,
    server_key=os.getenv("SERVER_KEY"),
    client_key=os.getenv("CLIENT_KEY"),
)


async def top_up(amount: int, db: Session, token: str):
    user = user = await utils.get_current_user(
        token=token,
        db=db,
    )
    _uuid = "top-up-" + str(uuid.uuid4())

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
                "email": user.email,
                "phone": user.phone_number,
            },
        }

        charge_response = core_api.charge(param)
        if charge_response:
            return charge_response
    return utils.credentials_exception


async def add_point(transaction_id: str, db: Session, token: str):
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    transaction = core_api.transactions.status(transaction_id)
    amount = int(float(transaction["gross_amount"]))
    transaction_status = transaction["transaction_status"]

    if user:
        if transaction_status == "settlement":
            user.point += amount
            db.commit()
            return True
    return False
