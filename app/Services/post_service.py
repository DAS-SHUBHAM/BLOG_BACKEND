import re
from sqlalchemy.orm import Session
from ..models.post import Post, Category, Tag
from ..Schemas.post_schema import PostCreate, PostUpdate

def slugify(text: str):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

def calculate_read_time(content: str):
    words_per_minute = 200
    words = len(content.split())
    return max(1, round(words / words_per_minute))

def create_new_post(db: Session, post_data: PostCreate, author_id: int):
    # Handle Category
    category_id = None
    if post_data.category_uuid:
        cat = db.query(Category).filter(Category.uuid == post_data.category_uuid).first()
        category_id = cat.id if cat else None

    # Handle Slug uniqueness
    base_slug = slugify(post_data.title)
    
    # --- THE FIX IS RIGHT HERE ---
    new_post = Post(
        author_id=author_id,
        category_id=category_id,
        title=post_data.title,
        slug=base_slug,
        content=post_data.content,
        summary=post_data.summary or post_data.content[:150] + "...",
        
        # Mapping the missing field from Pydantic input data to SQLAlchemy Model
        featured_image_url=post_data.featured_image_url, 
        
        read_time=calculate_read_time(post_data.content),
        status="published" # Or "draft" based on logic
    )
    
    # Handle Tags
    if post_data.tags:
        for tag_name in post_data.tags:
            tag_slug = slugify(tag_name)
            tag = db.query(Tag).filter(Tag.slug == tag_slug).first()
            if not tag:
                tag = Tag(name=tag_name, slug=tag_slug)
                db.add(tag)
                db.flush()
            new_post.tags.append(tag)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post