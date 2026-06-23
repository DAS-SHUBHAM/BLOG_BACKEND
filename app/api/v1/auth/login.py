from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime

from slowapi import Limiter
from slowapi.util import get_remote_address

# Absolute imports targeting your root app structure cleanly
from app.database import get_db
from app.core.security import create_access_token
from app.Services import auth_service
from app.Schemas.token_schema import Token
from app.models.user import User, OTPVerification

router = APIRouter()

# Initialize the local endpoint rate limiting instance
limiter = Limiter(key_func=get_remote_address)

@router.post("/login", response_model=Token)
@limiter.limit("10/minute")  # Prevents mass dictionary and credential-stuffing automated attacks
def login(
    request: Request,        # Required parameter for slowapi to parse client IP
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account not verified. Please verify your email."
        )
    
    access_token = create_access_token(subject=user.uuid)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-otp")
@limiter.limit("5/minute")  # Strict: Halts 6-digit number combinations guessing loops quickly
def verify_otp(
    request: Request,       # Required parameter for slowapi to parse client IP
    email: str, 
    otp_code: str, 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get the most recent OTP for this user
    db_otp = db.query(OTPVerification).filter(
        OTPVerification.user_id == user.id,
        OTPVerification.otp_code == otp_code
    ).order_by(OTPVerification.created_at.desc()).first()

    if not db_otp:
        raise HTTPException(status_code=400, detail="Invalid OTP code")
    
    # --- EXPIRY CHECK ---
    if db_otp.expires_at < datetime.now():
        db.delete(db_otp)  # Clean up expired OTP
        db.commit()
        raise HTTPException(status_code=400, detail="OTP has expired (10 min limit reached)")

    user.is_verified = True
    db.delete(db_otp) 
    db.commit()

    return {"message": "Email verified successfully!"}