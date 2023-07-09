from fastapi import Depends, APIRouter
from api.endpoint import get_db
from sqlalchemy.orm import Session
import xendit
from decouple import config
from fastapi.encoders import jsonable_encoder

xendit.api_key = config("API_KEY")

router = APIRouter()


@router.get("/xendit/test")
async def test():
    data = {
        "external_id": "YOUR_EXTERNAL_ID",
        "amount": 10000,  # Amount in IDR
        "phone": "YOUR_PHONE_NUMBER",  # Customer's phone number
        "callback_url": "YOUR_CALLBACK_URL",
    }

    payment = xendit.OVOPayment(**data)
    print(payment)
    return jsonable_encoder({"data": payment})
