from db.schemas import user as UserSchema
from sqlalchemy.orm import Session
from api.crud import user as UserCrud
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, APIRouter
from api.endpoint import get_db
import utils
from datetime import timedelta

router = APIRouter()


# type 3 = seller (mahasiswa), type 2 = buyer (pabrik)
@router.post("/register", response_model=UserSchema.UserResponse)
async def create_user(user: UserSchema.UserCreate, db: Session = Depends(get_db)):
    try:
        data = await UserCrud.register(db=db, user=user)
        access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = utils.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        if type(data) is not str and data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "register success",
                    "token": access_token,
                    "token_type": "bearer",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "register failed", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.post("/login", response_model=UserSchema.UserResponse)
async def read_user(user: UserSchema.UserLogin, db: Session = Depends(get_db)):
    try:
        data = await UserCrud.authenticate(
            db=db, username=user.username, password=user.password
        )

        access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = utils.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "authenticated",
                    "token": access_token,
                    "token_type": "bearer",
                    "data": data,
                }
            )
        return jsonable_encoder({"status_code": 401, "message": "user not found"})
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
