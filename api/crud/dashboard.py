from sqlalchemy.orm import Session
from db.models import advertisement as AdvertisementModel
from db.models import food_waste_category as CategoryModel
from db.models import transaction as TransactionModel
from db.models import user as UserModel
import utils
from sqlalchemy import func, desc


async def index(db: Session, token: str):
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        food_waste_categories = db.query(CategoryModel.FoodWasteCategory).all()
        category_weight_data = [
            {
                "category": category.name,
                "image": category.image,
                "total_weight": 0,
                "transaction_count": 0,
            }
            for category in food_waste_categories
        ]

        category_weights = (
            db.query(
                CategoryModel.FoodWasteCategory.name,
                func.sum(TransactionModel.Transaction.weight).label("total_weight"),
                func.count(TransactionModel.Transaction.id).label("transaction_count"),
            )
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
            .filter(TransactionModel.Transaction.user_id == user.id)
            .group_by(CategoryModel.FoodWasteCategory.name)
            .all()
        )

        for row in category_weights:
            category_name = row[0]
            for category_data in category_weight_data:
                if category_data["category"] == category_name:
                    category_data["total_weight"] = row[1]
                    category_data["transaction_count"] = row[2]
                    break

        return category_weight_data
    return utils.credentials_exception


async def recent_transaction(db: Session, token: str):
    user = await utils.get_current_user(token=token, db=db)

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
            .order_by(desc(TransactionModel.Transaction.created_at))
            .limit(5)
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
            .filter(AdvertisementModel.Advertisement.user_id == user.id)
            .order_by(desc(TransactionModel.Transaction.created_at))
            .limit(5)
            .all()
        )

    if user:
        for i in range(len(transactions)):
            transactions[i] = {
                "created_at": transactions[i].created_at,
                "status": transactions[i].status,
                "title": transactions[i].advertisement.name,
                "total_price": transactions[i].total_price,
                "user": transactions[i].advertisement.user.name,
                "image": transactions[i].advertisement.user.image,
            }
        return transactions
    return utils.credentials_exception
