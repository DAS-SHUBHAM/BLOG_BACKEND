from typing import List, Optional
from pydantic import BaseModel, ConfigDict, UUID4
from datetime import datetime
from .user_schema import UserResponse
from .category_schema import CategoryResponse

class TagBase(BaseModel):
    name: str

class TagResponse(TagBase):
    uuid: UUID4
    slug: str
    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    featured_image_url: Optional[str] = None

class PostCreate(PostBase):
    category_uuid: Optional[str] = None
    tags: List[str] = [] # List of tag names

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    featured_image_url: Optional[str] = None
    status: Optional[str] = None
    
class PostResponse(PostBase):
    uuid: UUID4
    slug: str
    status: str
    read_time: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    featured_image_url: Optional[str] = None
    author: UserResponse
    category: Optional[CategoryResponse] = None
    tags: List[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)