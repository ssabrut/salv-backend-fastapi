from sqlalchemy.orm import Session, joinedload
from db.models import advertisement as AdvertisementModel
from db.schemas import advertisement as AdvertisementSchema
from db.models import food_waste_category as CategoryModel
from db.models import user as UserModel
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
        .join(
            UserModel.User,
            UserModel.User.id == AdvertisementModel.Advertisement.user_id,
        )
        .filter(AdvertisementModel.Advertisement.status == "ongoing")
        .order_by(AdvertisementModel.Advertisement.created_at)
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
                .join(
                    CategoryModel.FoodWasteCategory,
                    AdvertisementModel.Advertisement.food_waste_category_id
                    == CategoryModel.FoodWasteCategory.id,
                )
                .join(
                    UserModel.User,
                    UserModel.User.id == AdvertisementModel.Advertisement.user_id,
                )
                .filter(AdvertisementModel.Advertisement.user_id == user.id)
                .order_by(AdvertisementModel.Advertisement.created_at)
                .all()
            )

        for i in range(len(advertisements)):
            advertisements[i] = {
                "id": advertisements[i].id,
                "title": advertisements[i].name,
                "category": advertisements[i].food_waste_category.name,
                "price": advertisements[i].price,
                "user": advertisements[i].user.name,
                "image": advertisements[i].user.image,
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
            "name": advertisement.name,
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
            "id": advertisement.id,
            "ongoing_weight": advertisement.ongoing_weight,
            "requested_weight": advertisement.requested_weight,
            "title": advertisement.name,
            "category": advertisement.food_waste_category.name,
            "additional_information": advertisement.additional_information,
            "maximum_weight": advertisement.maximum_weight,
            "minimum_weight": advertisement.minimum_weight,
            "price": advertisement.price,
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
                func.lower(AdvertisementModel.Advertisement.name).like(
                    "%" + query.lower() + "%"
                )
            )
            .order_by(AdvertisementModel.Advertisement.created_at)
            .all()
        )

        for i in range(len(advertisements)):
            advertisements[i] = {
                "id": advertisements[i].id,
                "title": advertisements[i].name,
                "category": advertisements[i].food_waste_category.name,
                "price": advertisements[i].price,
                "user": advertisements[i].user.name,
                "image": advertisements[i].user.image,
            }
        return advertisements
    return utils.credentials_exception


async def cancel(advertisement_id: str, db: Session, token: str):
    advertisement = (
        db.query(AdvertisementModel.Advertisement)
        .filter(AdvertisementModel.Advertisement.id == advertisement_id)
        .first()
    )

    user = await utils.get_current_user(token=token, db=db)

    if user:
        advertisement.status = "cancel"
        db.commit()
        return True
    return False


async def content_based(categories: list, db: Session, token: str):
    user = await utils.get_current_user(token=token, db=db)

    if user:
        data = []
        for category in categories:
            advertisements = (
                db.query(AdvertisementModel.Advertisement)
                .join(
                    CategoryModel.FoodWasteCategory,
                    AdvertisementModel.Advertisement.food_waste_category_id
                    == CategoryModel.FoodWasteCategory.id,
                )
                .filter(
                    func.lower(AdvertisementModel.Advertisement.name).like(
                        "%" + category.lower() + "%"
                    )
                )
                .order_by(AdvertisementModel.Advertisement.created_at)
                .all()
            )

            for advertisement in advertisements:
                if advertisement.status == "ongoing":
                    ads = {
                        "id": advertisement.id,
                        "title": advertisement.name,
                        "category": advertisement.food_waste_category.name,
                        "price": advertisement.price,
                        "user": advertisement.user.name,
                        "image": advertisement.user.image,
                    }
                    data.append(ads)
        return data
    return utils.credentials_exception
