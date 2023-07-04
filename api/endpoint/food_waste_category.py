from db.schemas import food_waste_category as CategorySchema
from fastapi import Depends, APIRouter
from api.endpoint import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.crud import food_waste_category as CategoryCrud

router = APIRouter()


@router.post('/food-waste-categories/create')
async def create_category(category: CategorySchema.FoodWasteCategory, db: Session = Depends(get_db)):
    try:
        data = await CategoryCrud.create(db=db, category=category)
    except Exception as e:
        return jsonable_encoder({'status_code': 500, 'message': str(e)})

@router.get(
    "/food-waste-categories", response_model=CategorySchema.FoodWasteCategoryResponse
)
async def read_category(db: Session = Depends(get_db)):
    try:
        data = await CategoryCrud.index(db)
        return jsonable_encoder(
            {"status_code": 200, "message": "success get all category", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
