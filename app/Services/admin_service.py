from sqlalchemy.orm import Session
from ..models.post import Category
from ..Schemas.category_schema import CategoryCreate
from .post_service import slugify

def create_category(db: Session, cat_data: CategoryCreate):
    slug = slugify(cat_data.name)
    new_cat = Category(name=cat_data.name, slug=slug)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

def get_all_categories(db: Session):
    return db.query(Category).all()