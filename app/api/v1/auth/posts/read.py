from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .....database import get_db
from .....Schemas.post_schema import PostResponse
from .....models.post import Post

router = APIRouter()

@router.get("/", response_model=List[PostResponse])
def read_posts(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    posts = db.query(Post).filter(Post.status == "published").offset(skip).limit(limit).all()
    return posts

@router.get("/{slug}", response_model=PostResponse)
def read_post_by_slug(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post