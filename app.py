from fastapi import FastAPI, Depends
from enum import Enum
from db.engine import Base, engine
from db.engine import Session as LocalSession
from db.schemas import user as UserSchema
from sqlalchemy.orm import Session
from api.crud import user as UserCrud
from fastapi.encoders import jsonable_encoder

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/users/", response_model=UserSchema.UserResponse)
async def create_user(user: UserSchema.UserCreate, db: Session = Depends(get_db)):
    data = UserCrud.create(db=db, user=user)
    return jsonable_encoder(
        {"status_code": 200, "message": "register success", "data": data}
    )
