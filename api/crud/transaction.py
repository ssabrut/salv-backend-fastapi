from sqlalchemy.orm import Session
from db.models import transaction as TransactionModel
from db.schemas import transaction as TransactionSchema
from db.models import advertisement as AdvertisementModel
from db.models import user as UserModel
from db.models import food_waste_category as CategoryModel
import uuid
import utils


async def index(db: Session, token: str):
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    transactions = (
        db.query(TransactionModel.Transaction)
        .join(
            AdvertisementModel.Advertisement,
            TransactionModel.Transaction.advertisement_id
            == AdvertisementModel.Advertisement.id,
        )
        .join(
            UserModel.User,
            AdvertisementModel.Advertisement.user_id == UserModel.User.id,
        )
        .filter(TransactionModel.Transaction.user_id == user.id)
        .all()
    )

    transactions.sort(key=lambda t: (t.status != 0 and t.status != 2, t.status))

    if user:
        for i in range(len(transactions)):
            transactions[i] = {
                "id": transactions[i].id,
                "title": transactions[i].advertisement.title,
                "user": transactions[i].user.name,
                "status": transactions[i].status,
                "total_price": transactions[i].total_price,
                "created_at": transactions[i].created_at,
                "image": transactions[i].image,
            }

        return transactions
    return utils.credentials_exception


async def create(
    db: Session, transaction: TransactionSchema.TransactionBase, token: str
):
    _uuid = str(uuid.uuid4())
    advertisement = (
        db.query(AdvertisementModel.Advertisement)
        .filter(AdvertisementModel.Advertisement.id == transaction.advertisement_id)
        .first()
    )

    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        if advertisement.ongoing_weight == advertisement.requested_weight:
            advertisement.status = "finished"
            return "advertisement has reached target"

        if (
            advertisement.ongoing_weight + transaction.weight
            <= advertisement.requested_weight
        ):
            data = {
                "id": _uuid,
                "user_id": user.id,
                "advertisement_id": transaction.advertisement_id,
                "retrieval_system": transaction.retrieval_system,
                "weight": transaction.weight,
                "location": transaction.location,
                "image": transaction.image,
                "total_price": transaction.weight * advertisement.price,
            }

            db_transaction = TransactionModel.Transaction(**data)
            advertisement.ongoing_weight += transaction.weight
            db.add(db_transaction)
            db.commit()
            db.refresh(db_transaction)
            return db_transaction
        return "weight exceed the target"
    return utils.credentials_exception


async def get(db: Session, transaction_id: str, token: str):
    transaction = (
        db.query(TransactionModel.Transaction)
        .join(
            AdvertisementModel.Advertisement,
            TransactionModel.Transaction.advertisement_id
            == AdvertisementModel.Advertisement.id,
        )
        .join(
            CategoryModel.FoodWasteCategory,
            AdvertisementModel.Advertisement.food_waste_category_id
            == CategoryModel.FoodWasteCategory.id,
        )
        .filter(TransactionModel.Transaction.id == transaction_id)
        .first()
    )

    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        data = {
            "id": transaction.id,
            "title": transaction.advertisement.title,
            "category": transaction.advertisement.food_waste_category.name,
            "additional_information": transaction.advertisement.additional_information,
            "minimum_weight": transaction.advertisement.minimum_weight,
            "maximum_weight": transaction.advertisement.maximum_weight,
            "price": transaction.advertisement.price,
            "weight": transaction.weight,
            "location": transaction.location,
            "image": transaction.image,
            "retrieval_system": transaction.retrieval_system,
            "total_price": transaction.total_price,
            "status": transaction.status,
        }
        return data
    return utils.credentials_exception


async def update(db: Session, transaction_id: str, status: int, token: str):
    transaction = (
        db.query(TransactionModel.Transaction)
        .filter(TransactionModel.Transaction.id == transaction_id)
        .first()
    )

    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        transaction.status = status
        db.commit()
        return transaction
    return utils.credentials_exception
