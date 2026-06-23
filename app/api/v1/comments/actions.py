from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....database import get_db
from ....api.deps import get_current_user
from ....Services import comments_service
from ....models.user import User

router = APIRouter()

@router.post("/{post_uuid}")
def post_comment(
    post_uuid: str, 
    content: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    comment = comments_service.add_comment(db, post_uuid, current_user.id, content)
    if not comment:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Comment added successfully", "uuid": comment.uuid}