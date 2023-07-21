from sqlalchemy.orm import Session, joinedload
from db.models import advertisement as AdvertisementModel
from db.schemas import advertisement as AdvertisementSchema
from db.models import food_waste_category as CategoryModel
import uuid
import utils
from sqlalchemy import func
from datetime import timedelta


async def index(db: Session, token: str):
    advertisements = (
        db.query(AdvertisementModel.Advertisement)
        .join(
            CategoryModel.FoodWasteCategory,
            AdvertisementModel.Advertisement.food_waste_category_id
            == CategoryModel.FoodWasteCategory.id,
        )
        .all()
    )
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        if user.type == 2:
            advertisements = (
                db.query(AdvertisementModel.Advertisement)
                .filter(AdvertisementModel.Advertisement.user_id == user.id)
                .all()
            )

            for i in range(len(advertisements)):
                advertisements[i] = {
                    "end_date": advertisements[i].created_at + timedelta(days=5),
                    "id": advertisements[i].id,
                    "ongoing_weight": advertisements[i].ongoing_weight,
                    "requested_weight": advertisements[i].requested_weight,
                    "title": advertisements[i].title,
                }
        else:
            for i in range(len(advertisements)):
                advertisements[i] = {
                    "category": advertisements[i].food_waste_category.name,
                    "id": advertisements[i].id,
                    "ongoing_weight": advertisements[i].ongoing_weight,
                    "price": advertisements[i].price,
                    "requested_weight": advertisements[i].requested_weight,
                    "title": advertisements[i].title,
                    "end_date": advertisements[i].created_at + timedelta(days=5),
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
            "user_id": user.id,
            "title": advertisement.title,
            "retrieval_system": advertisement.retrieval_system,
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
            "additional_information": advertisement.additional_information,
            "category": advertisement.food_waste_category.name,
            "id": advertisement.id,
            "location": advertisement.location,
            "maximum_weight": advertisement.maximum_weight,
            "minimum_weight": advertisement.minimum_weight,
            "ongoing_weight": advertisement.ongoing_weight,
            "price": advertisement.price,
            "retrieval_system": advertisement.retrieval_system,
            "title": advertisement.title,
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
            .join(
                CategoryModel.FoodWasteCategory,
                AdvertisementModel.Advertisement.food_waste_category_id
                == CategoryModel.FoodWasteCategory.id,
            )
            .filter(
                func.lower(AdvertisementModel.Advertisement.title).like(
                    "%" + query.lower() + "%"
                )
            )
            .all()
        )

        for i in range(len(advertisements)):
            advertisements[i] = {
                "category": advertisements[i].food_waste_category.name,
                "id": advertisements[i].id,
                "ongoing_weight": advertisements[i].ongoing_weight,
                "price": advertisements[i].price,
                "requested_weight": advertisements[i].requested_weight,
                "title": advertisements[i].title,
                "end_date": advertisements[i].created_at + timedelta(days=5),
            }
        return advertisements
    return utils.credentials_exception
