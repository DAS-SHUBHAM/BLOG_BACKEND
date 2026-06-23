from sqlalchemy import Table, Column, Integer, ForeignKey
from ..database import Base

# Bridge table for many-to-many relationship between Posts and Tags
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)
)