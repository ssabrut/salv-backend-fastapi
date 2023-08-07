from sqlalchemy.orm import Session
from db.models import transaction as TransactionModel
from db.schemas import transaction as TransactionSchema
from db.models import advertisement as AdvertisementModel
from db.models import user as UserModel
from db.models import food_waste_category as CategoryModel
from sqlalchemy import desc
import uuid
import utils


async def index(db: Session, token: str):
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user.type == 3:
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
            .order_by(
                desc(TransactionModel.Transaction.created_at),
            )
            .all()
        )
    else:
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
            .filter(TransactionModel.Transaction.advertisement.id == user.id)
            .order_by(
                desc(TransactionModel.Transaction.created_at),
            )
            .all()
        )

    transactions.sort(key=lambda t: (t.status != "0" and t.status != "1", t.status))

    if user:
        if user.type == 2:
            for i in range(len(transactions)):
                transactions[i] = {
                    "id": transactions[i].id,
                    "status": transactions[i].status,
                    "title": transactions[i].advertisement.name,
                    "user": transactions[i].advertisement.user.name,
                    "image": transactions[i].advertisement.user.image,
                    "weight": transactions[i].weight,
                    "created_at": transactions[i].created_at,
                }
        else:
            for i in range(len(transactions)):
                transactions[i] = {
                    "id": transactions[i].id,
                    "status": transactions[i].status,
                    "total_price": transactions[i].total_price,
                    "title": transactions[i].advertisement.name,
                    "user": transactions[i].advertisement.user.name,
                    "image": transactions[i].advertisement.user.image,
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
                "weight": transaction.weight,
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
        .join(UserModel.User, TransactionModel.Transaction.user_id == UserModel.User.id)
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
            "ongoing_weight": transaction.advertisement.ongoing_weight,
            "requested_weight": transaction.advertisement.requested_weight,
            "title": transaction.advertisement.name,
            "category": transaction.advertisement.food_waste_category.name,
            "additional_information": transaction.advertisement.additional_information,
            "weight": transaction.weight,
            "total_price": transaction.total_price,
        }

        if user.type == 2:
            data["latitude"] = transaction.user.latitude
            data["longitude"] = transaction.user.longitude
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

        if transaction.status == "2":
            seller = (
                db.query(UserModel.User)
                .filter(UserModel.User.id == transaction.user_id)
                .first()
            )

            buyer = (
                db.query(UserModel.User)
                .filter(UserModel.User.id == transaction.advertisement.user_id)
                .first()
            )

            seller.point += transaction.total_price
            db.commit()

            buyer.point -= transaction.total_price
            db.commit()
        return transaction
    return utils.credentials_exception
