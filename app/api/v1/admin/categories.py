from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ....database import get_db
from ....api.deps import allow_admin_only
from ....Schemas.category_schema import CategoryCreate, CategoryResponse
from ....Services import admin_service

router = APIRouter()

@router.post("/", response_model=CategoryResponse)
def add_category(
    cat_in: CategoryCreate, 
    db: Session = Depends(get_db), 
    admin=Depends(allow_admin_only)
):
    return admin_service.create_category(db, cat_data=cat_in)