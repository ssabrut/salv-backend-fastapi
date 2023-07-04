from db.schemas import user as UserSchema
from sqlalchemy.orm import Session
from api.crud import user as UserCrud
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, APIRouter
from api.endpoint import get_db

router = APIRouter()


@router.post("/register", response_model=UserSchema.UserResponse)
async def create_user(user: UserSchema.UserCreate, db: Session = Depends(get_db)):
    try:
        data = await UserCrud.register(db=db, user=user)
        return jsonable_encoder(
            {"status_code": 200, "message": "register success", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.post("/login", response_model=UserSchema.UserResponse)
async def read_user(user: UserSchema.UserLogin, db: Session = Depends(get_db)):
    try:
        data = await UserCrud.authenticate(
            db=db, username=user.username, password=user.password
        )

        if data:
            return jsonable_encoder(
                {"status_code": 200, "message": "authenticated", "data": data}
            )
        else:
            return jsonable_encoder({"status_code": 401, "message": "user not found"})
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
