from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import SessionLocal
from backend.app.models.post import Post
from backend.app.schemas.post import PostCreate
from backend.app.routes.auth import get_current_user
from backend.app.models.user import User


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_post = Post(
        caption=post.caption,
        image_url=post.image_url,
        user_id=current_user.id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "message": "Post created successfully",
        "post_id": new_post.id,
        "caption": new_post.caption,
        "image_url": new_post.image_url,
        "user_id": new_post.user_id,
    }
    
@router.get("/")
def get_posts(
    db: Session = Depends(get_db),
):
    posts = db.query(Post).order_by(Post.created_at.desc()).all()

    return [
        {
            "post_id": post.id,
            "caption": post.caption,
            "image_url": post.image_url,
            "user_id": post.user_id,
            "created_at": post.created_at,
        }
        for post in posts
    ]
    
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = (
        db.query(Post)
        .filter(
            Post.id == post_id,
            Post.user_id == current_user.id,
        )
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    db.delete(post)
    db.commit()

    return {
        "message": "Post deleted successfully",
        "post_id": post_id,
    }
    
@router.put("/{post_id}")
def update_post(
    post_id: int,
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = (
        db.query(Post)
        .filter(
            Post.id == post_id,
            Post.user_id == current_user.id,
        )
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    post.caption = post_data.caption
    post.image_url = post_data.image_url

    db.commit()
    db.refresh(post)

    return {
        "message": "Post updated successfully",
        "post_id": post.id,
        "caption": post.caption,
        "image_url": post.image_url,
    }