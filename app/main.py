from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .core.config import settings
from .database import engine, Base

# Import Version 1 Routers
from .api.v1.auth import signup, login
from .api.v1.auth.posts import create, read, update, delete
from .api.v1.admin import categories
from .api.v1.comments import actions

# Initialize Rate Limiter using the client's IP address
limiter = Limiter(key_func=get_remote_address)

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Production-ready backend for MithilaRoots Blog using FastAPI and MySQL"
)

# --- Attach Limiter State to App ---
app.state.limiter = limiter
# Custom handler to return a clean JSON error when someone hits the rate limit
@app.exception_handler(RateLimitExceeded)
def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please slow down and try again later."}
    )

# --- Middleware Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Version 1 Route Registrations ---
app.include_router(signup.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(login.router, prefix="/api/v1/auth", tags=["Authentication"])

app.include_router(create.router, prefix="/api/v1/posts", tags=["Posts"])
app.include_router(read.router, prefix="/api/v1/posts", tags=["Posts"])
app.include_router(update.router, prefix="/api/v1/posts", tags=["Posts"])
app.include_router(delete.router, prefix="/api/v1/posts", tags=["Posts"])

app.include_router(categories.router, prefix="/api/v1/admin/categories", tags=["Admin"])
app.include_router(actions.router, prefix="/api/v1/comments", tags=["Comments"])

@app.get("/", tags=["Health"])
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }