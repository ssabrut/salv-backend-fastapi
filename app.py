from fastapi import FastAPI
from db.engine import Base, engine
from api.endpoint.user import router as user_router
from api.endpoint.food_waste_category import router as category_router
from api.endpoint.advertisement import router as advertisement_router


Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


app.include_router(user_router)
app.include_router(category_router)
app.include_router(advertisement_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
