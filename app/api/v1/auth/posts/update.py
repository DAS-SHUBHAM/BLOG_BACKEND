from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .....database import get_db
from .....api.deps import get_current_user
from .....Schemas.post_schema import PostUpdate, PostResponse
from .....models.post import Post
from .....models.user import User

router = APIRouter()

@router.put("/{uuid}", response_model=PostResponse)
def update_post(
    uuid: str, 
    post_in: PostUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_post = db.query(Post).filter(Post.uuid == uuid).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check ownership
    if db_post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    update_data = post_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post

