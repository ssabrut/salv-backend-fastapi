from sqlalchemy.orm import Session, joinedload
from db.models import transaction as TransactionModel
from db.schemas import transaction as TransactionSchema
from db.models import advertisement as AdvertisementModel
import uuid


async def index(db: Session, user_id: str):
    transactions = (
        db.query(TransactionModel.Transaction)
        .join(
            AdvertisementModel.Advertisement,
            TransactionModel.Transaction.advertisement_id
            == AdvertisementModel.Advertisement.id,
        )
        .filter(TransactionModel.Transaction.user_id == user_id)
        .all()
    )

    # for i in range(len(transactions)):
    #     transactions[i] = {
    #         "id": transactions[i].id,
    #         "title": transactions[i].advertisement.title,
    #     }

    return transactions


async def create(db: Session, transaction: TransactionSchema.TransactionBase):
    _uuid = str(uuid.uuid4())
    advertisement = (
        db.query(AdvertisementModel.Advertisement)
        .filter(AdvertisementModel.Advertisement.id == transaction.advertisement_id)
        .first()
    )

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
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
