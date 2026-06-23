import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fetch database URL from environment or fallback safely
# Ensure your .env file contains: DATABASE_URL=postgresql+psycopg2://...
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing in your configuration!")

# Create the SQLAlchemy engine optimized for Neon Cloud PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Critical for Cloud: Verifies the socket connection hasn't dropped before running a query
    pool_recycle=300     # Recycles idle connections every 5 minutes to stay lightweight on Neon's compute lifecycle
)

# Session factory linked to the new engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to inherit from
Base = declarative_base()

# Dependency to yield a clean database connection session for each incoming API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()