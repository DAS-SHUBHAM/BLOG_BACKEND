import uuid
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID  # Native PostgreSQL UUID support
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from .associations import post_tags

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    
    # Upgraded to Native Postgres UUID type
    uuid = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(100), unique=True, index=True)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Upgraded to Native Postgres UUID type
    uuid = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String(500), nullable=True)
    featured_image_url = Column(String(255), nullable=True)
    
    # FIXED: Added name='post_status_enum' to satisfy PostgreSQL requirements!
    status = Column(
        Enum('draft', 'published', name='post_status_enum'), 
        default='draft',
        nullable=False
    )
    
    read_time = Column(Integer, default=1)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    author = relationship("User")
    category = relationship("Category")
    tags = relationship("Tag", secondary=post_tags)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    
    # Upgraded to Native Postgres UUID type
    uuid = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(100), unique=True, index=True)