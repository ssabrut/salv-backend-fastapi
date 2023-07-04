from db.schemas import advertisement as AdvertisementSchema
from fastapi import Depends, APIRouter
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import advertisement as AdvertisementCrud

router = APIRouter()


@router.post("/advertisements/create")
async def create_advertisement(
    advertisement: AdvertisementSchema.AdvertisementBase, db: Session = Depends(get_db)
):
    try:
        data = await AdvertisementCrud.create(db=db, advertisement=advertisement)

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "success to create advertisement",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {
                "status_code": 400,
                "message": "failed to create advertisement",
            }
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
