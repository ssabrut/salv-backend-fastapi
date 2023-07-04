from sqlalchemy.orm import Session, joinedload
from db.models import advertisement as AdvertisementModel
from db.schemas import advertisement as AdvertisementSchema
from db.models import user as UserModel
import uuid


async def index(db: Session, user_id: str):
    user = db.query(UserModel.User).filter(UserModel.User.id == user_id).first()
    if user.type == 2:
        advertisements = (
            db.query(AdvertisementModel.Advertisement)
            .filter(AdvertisementModel.Advertisement.user_id == user_id)
            .all()
        )
        return advertisements


async def create(db: Session, advertisement: AdvertisementSchema.AdvertisementBase):
    _uuid = str(uuid.uuid4())
    data = {
        "id": _uuid,
        "food_waste_category_id": advertisement.food_waste_category_id,
        "user_id": advertisement.user_id,
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


async def get(db: Session, advertisement_id: str):
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
        "retrieval_system": advertisement.retrieval_system,
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
