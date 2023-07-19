from sqlalchemy.orm import Session
from db.schemas import user as UserSchema
from db.models import user as UserModel
import uuid
from utils import get_password_hash, verify_password
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("salv-4c518-firebase-adminsdk-h5rg2-6b49c4820c.json")
firebase_admin.initialize_app(cred)


async def register(db: Session, user: UserSchema.UserCreate):
    _uuid = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)
    if (
        db.query(UserModel.User)
        .filter(UserModel.User.username == user.username)
        .first()
    ):
        return "username exist"

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
        "province": user.province,
        "city": user.city,
        "subdistrict": user.subdistrict,
        "ward": user.ward,
        "address": user.address,
        "postal_code": user.postal_code,
        "image": user.image if user.image else "",
        "latitude": user.latitude if user.latitude else 0,
        "longitude": user.longitude if user.longitude else 0,
    }

    db_user = UserModel.User(**data)
    db.add(db_user)
    db.commit()

    auth.create_user(email=user.email, password=user.password)
    db.refresh(db_user)
    return db_user


async def authenticate(db: Session, username: str, password: str = ""):
    user = db.query(UserModel.User).filter(UserModel.User.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.password) and password != "":
        return False
    return user
