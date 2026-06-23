import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load the .env file from the root directory
load_dotenv()

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "MithilaRoots Blog")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:pass@localhost/db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "6416cd210196c5021057d5705c36f8d3647b5349914b7b5db3ba16c85393f5b")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10080))
    
    # Mail Settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")

    # Media settings for blog images
    UPLOAD_DIR: str = "static/uploads"

    # Modern Pydantic Config - Corrected import and removed syntax error
    model_config = SettingsConfigDict(
        case_sensitive=True, 
        env_file=".env",
        extra="ignore"
    )

settings = Settings()