from sqlalchemy.orm import Session, joinedload
from db.models import advertisement as AdvertisementModel
from db.models import food_waste_category as CategoryModel
from db.models import transaction as TransactionModel
from db.models import user as UserModel
import uuid
import utils
from sqlalchemy import func
from datetime import timedelta


async def index(db: Session, token: str):
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    food_waste_categories = db.query(CategoryModel.FoodWasteCategory).all()
    category_weight_data = [
        {
            "food_waste_category_name": category.name,
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
            if category_data["food_waste_category_name"] == category_name:
                category_data["total_weight"] = row[1]
                category_data["transaction_count"] = row[2]
                break

    return category_weight_data if category_weight_data else "no data"
