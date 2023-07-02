from sqlalchemy.orm import Session
from db.schemas import user as UserSchema
from db.models import user as UserModel


def create(db: Session, user: UserSchema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = UserModel.User(
        id="asd21fgag",
        type=0,
        name="Achmad Rijalu",
        username="asd2g",
        password=fake_hashed_password,
        phone_number="120497123",
        province="Jawa Timur",
        city="Surabaya",
        subdistrict="Sambikerep",
        ward="Sambikerep",
        address="Test",
        postal_code="60129",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
