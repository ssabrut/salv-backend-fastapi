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
    _uuid = "top-up-" + str(uuid.uuid4())
    user = user = await utils.get_current_user(
        token=token,
        db=db,
    )

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
            # await InvoiceCrud.create_invoice(
            #     user_id=user.id, order_id=_uuid, amount=amount, db=db
            # )
            return charge_response
    return utils.credentials_exception
