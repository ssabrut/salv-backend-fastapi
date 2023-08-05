from db.schemas import advertisement as AdvertisementSchema
from fastapi import Depends, APIRouter, Request
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import dashboard as DashboardCrud
import utils

router = APIRouter()


@router.get("/dashboard")
async def index(request: Request, db: Session = Depends(get_db)):
    try:
        token = utils.get_token(request)
        data = await DashboardCrud.index(db=db, token=token)
        recent_transaction = await DashboardCrud.recent_transaction(db=db, token=token)

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
                    "message": "success getting report",
                    "data": data,
                    "transactions": recent_transaction,
                }
            )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
