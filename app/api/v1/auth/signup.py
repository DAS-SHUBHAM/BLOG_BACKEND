from fastapi import APIRouter, Depends, status, BackgroundTasks, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

# Absolute imports starting from the root 'app' module
from app.database import get_db
from app.Schemas.user_schema import UserCreate, UserResponse
from app.Services import auth_service

router = APIRouter()

# Initialize the local file instance of the limiter tracking client IPs
limiter = Limiter(key_func=get_remote_address)

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # Strict protection: Max 5 account creation attempts per minute per IP
def signup(
    request: Request,               # Required by slowapi to capture the client's IP address
    user_in: UserCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    # 1. Create the user and generate OTP inside the service
    new_user = auth_service.create_user(db, user_data=user_in)
    
    # 2. Add the email sending to background tasks 
    # (Assuming you have a send_verification_email function)
    # background_tasks.add_task(auth_service.send_verification_email, new_user.email, db)
    
    return new_user