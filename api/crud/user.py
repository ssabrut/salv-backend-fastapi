from sqlalchemy.orm import Session
from db.schemas import user as UserSchema
from db.models import user as UserModel
import uuid
from utils import get_password_hash, verify_password
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from db.models.user import Address
import utils

cred = credentials.Certificate("salv-amcc-firebase-adminsdk-bq8va-773dfd1fd6.json")
firebase_admin.initialize_app(cred)


async def is_address_exist(db: Session, token: str):
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    address = (
        db.query(Address)
        .join(UserModel.User, Address.user_id == UserModel.User.id)
        .filter(Address.user_id == user.id)
        .first()
    )

    if user:
        return address
    return utils.credentials_exception


async def register(db: Session, user: UserSchema.UserCreate):
    _uuid = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)

    if (
        db.query(UserModel.User)
        .filter(UserModel.User.username == user.username)
        .first()
    ):
        return "username exist"

    if db.query(UserModel.User).filter(UserModel.User.email == user.email).first():
        return "email exist"

    while db.query(UserModel.User).filter(UserModel.User.id == _uuid).first():
        _uuid = str(uuid.uuid4())

    data = {
        "id": _uuid,
        "type": user.type,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "phone_number": user.phone_number,
        "image": user.image if user.image else "",
    }

    db_user = UserModel.User(**data)
    db.add(db_user)
    db.commit()

    # auth.create_user(email=user.email, password=user.password, uid=_uuid)
    db.refresh(db_user)
    return db_user


async def authenticate(db: Session, username: str, password: str = ""):
    user = db.query(UserModel.User).filter(UserModel.User.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.password) and password != "":
        return False
    return user


async def create_address(db: Session, address: Address, token: str):
    user = await utils.get_current_user(
        token=token,
        db=db,
    )

    if user:
        db_address = Address(
            user_id=user.id,
            province=address.province,
            city=address.city,
            subdistrict=address.subdistrict,
            ward=address.ward,
            address=address.address,
            postal_code=address.postal_code,
            latitude=address.latitude,
            longitude=address.longitude,
        )
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    return utils.credentials_exception
