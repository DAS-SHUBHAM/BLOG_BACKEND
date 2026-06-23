from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .....database import get_db
from .....api.deps import get_current_user
from .....models.post import Post
from .....models.user import User

router = APIRouter()

@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    uuid: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_post = db.query(Post).filter(Post.uuid == uuid).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Only the author or an admin can delete
    if db_post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(db_post)
    db.commit()
    return None