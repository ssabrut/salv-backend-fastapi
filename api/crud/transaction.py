from sqlalchemy.orm import Session
from db.models import transaction as TransactionModel
from db.schemas import transaction as TransactionSchema
from db.models import advertisement as AdvertisementModel
from db.models import user as UserModel
import uuid
import utils


async def index(db: Session, user_id: str, token: str):
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
        .filter(TransactionModel.Transaction.user_id == user_id)
        .all()
    )

    transactions.sort(key=lambda t: (t.status != 0 and t.status != 2, t.status))
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

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


async def create(db: Session, transaction: TransactionSchema.TransactionBase):
    _uuid = str(uuid.uuid4())
    advertisement = (
        db.query(AdvertisementModel.Advertisement)
        .filter(AdvertisementModel.Advertisement.id == transaction.advertisement_id)
        .first()
    )

    if advertisement.ongoing_weight == advertisement.requested_weight:
        advertisement.status = "finished"
        return "advertisement has reached target"

    if (
        advertisement.ongoing_weight + transaction.weight
        <= advertisement.requested_weight
    ):
        data = {
            "id": _uuid,
            "user_id": transaction.user_id,
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


async def top_up(db: Session, user_id: str):
    pass
