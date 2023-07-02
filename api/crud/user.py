from sqlalchemy.orm import Session
from db.schemas import user as UserSchema
from db.models import user as UserModel
import uuid
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create(db: Session, user: UserSchema.UserCreate):
    _uuid = str(uuid.uuid4())
    hashed_password = password_context.hash(user.password)
    data = {
        "id": _uuid,
        "type": user.type,
        "name": user.name,
        "username": user.username,
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
    db.refresh(db_user)
    return db_user
