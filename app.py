from fastapi import FastAPI
from enum import Enum
from db.engine import Base, engine, Session

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = Session()
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
