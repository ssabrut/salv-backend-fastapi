from fastapi import FastAPI
from db.engine import Base, engine
from api.endpoint.user import router as user_router
from api.endpoint.food_waste_category import router as category_router
from api.endpoint.advertisement import router as advertisement_router
from api.endpoint.transaction import router as transaction_router
from api.endpoint.midtrans import router as midtrans_router

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


app.include_router(user_router)
app.include_router(category_router)
app.include_router(advertisement_router)
app.include_router(transaction_router)
app.include_router(midtrans_router)
