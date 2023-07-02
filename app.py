from fastapi import FastAPI, Depends
from enum import Enum
from db.engine import Base, engine
from db.engine import Session as LocalSession
from db.schemas import user as UserSchema
from sqlalchemy.orm import Session
from api.crud import user as UserCrud

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# @app.get("/")
# async def root():
#     return {"message": "Hello"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name}

    if model_name.value == "lenet":
        return {"model_name": model_name}
    return {"model_name": model_name}


@app.post("/users/", response_model=UserSchema.User)
def create_user(user: UserSchema.UserCreate, db: Session = Depends(get_db)):
    return UserCrud.create(db=db, user=user)
