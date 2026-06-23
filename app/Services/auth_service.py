import os
import random
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv

from app.models.user import User, OTPVerification
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from app.core.security import verify_password

# Load the .env file
load_dotenv()

# Pulling info from .env
SMTP_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("MAIL_PORT", 587))
SENDER_EMAIL = os.getenv("MAIL_USERNAME")
SENDER_PASSWORD = os.getenv("MAIL_PASSWORD") # This should be your App Password

def send_otp_email(receiver_email: str, otp_code: str):
    msg = EmailMessage()
    msg["Subject"] = "MithilaRoots - Verify Your Account"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg.set_content(f"Your verification code is: {otp_code}\n\nThis code expires in 10 minutes.")

    try:
        # Using a context manager for a clean connection
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"DEBUG: OTP {otp_code} sent to {receiver_email}")
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to send email: {e}")

def create_user(db: Session, user_data):
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        is_verified=False
    )
    db.add(db_user)
    db.flush()

    otp_code = f"{random.randint(100000, 999999)}"
    expiry = datetime.now() + timedelta(minutes=10)
    
    db_otp = OTPVerification(
        user_id=db_user.id,
        otp_code=otp_code,
        expires_at=expiry
    )
    db.add(db_otp)
    db.commit()
    db.refresh(db_user)

    # Trigger the background email send
    send_otp_email(db_user.email, otp_code)
    
    return db_user

from app.core.security import verify_password # Make sure to import this at the top

def authenticate_user(db: Session, email: str, password: str):
    # 1. Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    # 2. Verify the hashed password
    if not verify_password(password, user.password_hash):
        return None
        
    return user