from fastapi import FastAPI
from db.engine import Base, engine
from api.endpoint.user import router


Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
