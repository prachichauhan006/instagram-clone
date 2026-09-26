from fastapi import FastAPI
from backend.app.db.database import Base, engine
from backend.app.models.user import User
from backend.app.routes.auth import router as auth_router

app = FastAPI(title="Instagram Clone")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Welcome to Instagram Clone API!"}