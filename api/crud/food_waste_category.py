from sqlalchemy.orm import Session
from db.models import food_waste_category as CategoryModel
from db.schemas import food_waste_category as CategorySchema
import uuid


async def index(db: Session):
    categories = db.query(CategoryModel.FoodWasteCategory).all()
    return categories


async def create(db: Session, category: CategorySchema.FoodWasteCategory):
    _uuid = str(uuid.uuid4())
    data = {"id": _uuid, "name": category.name}
    db_category = CategoryModel.FoodWasteCategory(**data)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
