from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import SessionLocal
from backend.app.models.like import Like
from backend.app.models.post import Post
from backend.app.models.user import User
from backend.app.routes.auth import get_current_user


router = APIRouter(
    prefix="/likes",
    tags=["Likes"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{post_id}")
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    existing_like = (
        db.query(Like)
        .filter(
            Like.user_id == current_user.id,
            Like.post_id == post_id,
        )
        .first()
    )

    if existing_like:
        raise HTTPException(
            status_code=400,
            detail="Post already liked",
        )

    new_like = Like(
        user_id=current_user.id,
        post_id=post_id,
    )

    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    return {
        "message": "Post liked successfully",
        "post_id": post_id,
        "user_id": current_user.id,
    }
    
@router.delete("/{post_id}")
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    like = (
        db.query(Like)
        .filter(
            Like.user_id == current_user.id,
            Like.post_id == post_id,
        )
        .first()
    )

    if not like:
        raise HTTPException(
            status_code=404,
            detail="Like not found",
        )

    db.delete(like)
    db.commit()

    return {
        "message": "Post unliked successfully",
        "post_id": post_id,
        "user_id": current_user.id,
    }
    
@router.get("/{post_id}")
def get_like_count(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    like_count = (
        db.query(Like)
        .filter(Like.post_id == post_id)
        .count()
    )

    return {
        "post_id": post_id,
        "like_count": like_count,
    }