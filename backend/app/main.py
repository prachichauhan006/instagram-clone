from fastapi import FastAPI

from backend.app.db.database import Base, engine

from backend.app.models.user import User
from backend.app.models.post import Post
from backend.app.models.like import Like

from backend.app.routes.auth import router as auth_router
from backend.app.routes.posts import router as posts_router
from backend.app.routes.likes import router as likes_router


app = FastAPI(title="Instagram Clone")


Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(likes_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Instagram Clone API!"
    }