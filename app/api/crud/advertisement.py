from sqlalchemy.orm import Session, joinedload
from db.models import advertisement as AdvertisementModel
from db.schemas import advertisement as AdvertisementSchema
import uuid
import utils
from sqlalchemy import func


async def index(db: Session, user_id: str, token: str):
    advertisements = db.query(AdvertisementModel.Advertisement).all()
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        if user.type == 2:
            advertisements = (
                db.query(AdvertisementModel.Advertisement)
                .filter(AdvertisementModel.Advertisement.user_id == user_id)
                .all()
            )

        for i in range(len(advertisements)):
            advertisements[i] = {
                "id": advertisements[i].id,
                "ongoing_weight": advertisements[i].ongoing_weight,
                "minimum_weight": advertisements[i].minimum_weight,
                "title": advertisements[i].title,
                "price": advertisements[i].price,
                "requested_weight": advertisements[i].requested_weight,
                "maximum_weight": advertisements[i].maximum_weight,
            }

        return advertisements
    return utils.credentials_exception


async def create(
    db: Session, advertisement: AdvertisementSchema.AdvertisementBase, token: str
):
    _uuid = str(uuid.uuid4())
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        data = {
            "id": _uuid,
            "food_waste_category_id": advertisement.food_waste_category_id,
            "user_id": advertisement.user_id,
            "title": advertisement.title,
            "location": advertisement.location,
            "additional_information": advertisement.additional_information
            if advertisement.additional_information
            else "",
            "price": advertisement.price,
            "requested_weight": advertisement.requested_weight,
            "minimum_weight": advertisement.minimum_weight,
            "maximum_weight": advertisement.maximum_weight,
        }

        db_advertisement = AdvertisementModel.Advertisement(**data)
        db.add(db_advertisement)
        db.commit()
        db.refresh(db_advertisement)
        return db_advertisement
    return utils.credentials_exception


async def get(db: Session, advertisement_id: str, token: str):
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        advertisement = (
            db.query(AdvertisementModel.Advertisement)
            .options(joinedload(AdvertisementModel.Advertisement.food_waste_category))
            .options(joinedload(AdvertisementModel.Advertisement.user))
            .filter(AdvertisementModel.Advertisement.id == advertisement_id)
            .first()
        )

        advertisement = {
            "id": advertisement.id,
            "status": advertisement.status,
            "additional_information": advertisement.additional_information,
            "ongoing_weight": advertisement.ongoing_weight,
            "minimum_weight": advertisement.minimum_weight,
            "title": advertisement.title,
            "location": advertisement.location,
            "price": advertisement.price,
            "requested_weight": advertisement.requested_weight,
            "maximum_weight": advertisement.maximum_weight,
            "user": advertisement.user.name,
            "category": advertisement.food_waste_category.name,
        }

        if not advertisement:
            return False
        return advertisement
    return utils.credentials_exception


async def search(db: Session, query: str, token: str):
    user = await utils.get_current_user(token=token, db=db)

    if user:
        advertisements = (
            db.query(AdvertisementModel.Advertisement)
            .filter(
                func.lower(AdvertisementModel.Advertisement.title).like(
                    "%" + query.lower() + "%"
                )
            )
            .all()
        )

        for i in range(len(advertisements)):
            advertisements[i] = {
                "id": advertisements[i].id,
                "ongoing_weight": advertisements[i].ongoing_weight,
                "minimum_weight": advertisements[i].minimum_weight,
                "title": advertisements[i].title,
                "price": advertisements[i].price,
                "requested_weight": advertisements[i].requested_weight,
                "maximum_weight": advertisements[i].maximum_weight,
            }
        return advertisements
    return utils.credentials_exception
