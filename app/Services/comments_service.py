from sqlalchemy.orm import Session
from ..models.comment import Comment
from ..models.post import Post

def add_comment(db: Session, post_uuid: str, user_id: int, content: str):
    post = db.query(Post).filter(Post.uuid == post_uuid).first()
    if not post:
        return None
    
    new_comment = Comment(
        post_id=post.id,
        user_id=user_id,
        content=content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment