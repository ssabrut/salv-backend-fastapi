from db.schemas import user as UserSchema
from sqlalchemy.orm import Session
from api.crud import user as UserCrud
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, APIRouter, Request
from api.endpoint import get_db
import utils
from datetime import timedelta

router = APIRouter()


# type 3 = seller (mahasiswa), type 2 = buyer (pabrik)
@router.post("/register")
async def create_user(user: UserSchema.UserCreate, db: Session = Depends(get_db)):
    try:
        data = await UserCrud.register(db=db, user=user)
        access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = utils.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        if type(data) is not str and data:
            data = data.__dict__
            data["token"] = access_token

            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "register success",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "register failed", "data": data}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.post("/login")
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
            data = data.__dict__
            data["token"] = access_token

            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "authenticated",
                    "data": data,
                }
            )
        return jsonable_encoder({"status_code": 401, "message": "user not found"})
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})


@router.post("/logout")
async def destroy_session(request: Request, db: Session = Depends(get_db)):
    token = utils.get_token(request)
    if token:
        utils.revoke_token(token, db)
        return jsonable_encoder(
            {
                "status_code": 200,
                "message": "token revoked",
            }
        )


@router.post("/address/create")
async def create_address(
    address: UserSchema.AddressBase, request: Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await UserCrud.create_address(db=db, address=address, token=token)
        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "address created",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "address failed to create"}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})

@router.post("/address/update")
async def update_address(
    updated_location: UserSchema.AddressUpdate, request:Request, db: Session = Depends(get_db)
):
    try:
        token = utils.get_token(request)
        data = await UserCrud.update_address(db=db, updated_location=updated_location, token=token)
        if data:
            return jsonable_encoder(
                {
                    "status_code": 200,
                    "message": "Address Updated",
                    "data": data,
                }
            )
        return jsonable_encoder(
            {"status_code": 400, "message": "Address failed to update"}
        )
    except Exception as e:
        return jsonable_encoder({"status_code": 500, "message": str(e)})
