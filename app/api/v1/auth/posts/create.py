from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

# Absolute imports starting from the 'app' directory
from app.database import get_db
from app.api.deps import get_current_user
from app.Schemas.post_schema import PostCreate, PostResponse
from app.Services import post_service
from app.models.user import User

router = APIRouter()

# Initialize the local file instance of the limiter tracking client IPs
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/hour")  # Protects your MySQL disk from automated post spamming
def create_post(
    request: Request,       # Required parameter for slowapi to parse client IP
    post_in: PostCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # This remains the same because post_in now successfully passes the image through
    return post_service.create_new_post(db, post_data=post_in, author_id=current_user.id)