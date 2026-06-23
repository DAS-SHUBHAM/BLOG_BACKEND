import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load env variables
load_dotenv()

# Import models 
from app.models.user import User
from app.models.post import Post, Category, Tag
from app.models.comment import Comment
from app.database import Base

# 1. Configuration
MYSQL_URL = os.getenv("MYSQL_URL", "mysql+pymysql://root:root@localhost:3306/blog_db")
NEON_URL = os.getenv("DATABASE_URL")

# 2. Engines
mysql_engine = create_engine(MYSQL_URL)
neon_engine = create_engine(NEON_URL)

MySQLSession = sessionmaker(bind=mysql_engine)
NeonSession = sessionmaker(bind=neon_engine)

def migrate():
    old_db = MySQLSession()
    new_db = NeonSession()

    print("--- Starting Migration ---")

    try:
        # Maps to store old_id : new_id
        user_map = {}
        category_map = {}
        post_map = {}

        # A. Migrate Categories
        for cat in old_db.query(Category).all():
            new_cat = Category(name=cat.name, slug=cat.slug, uuid=cat.uuid)
            new_db.add(new_cat)
            new_db.flush()
            category_map[cat.id] = new_cat.id 
        print("Categories migrated.")

        # B. Migrate Users
        for user in old_db.query(User).all():
            new_user = User(
                username=user.username, email=user.email, 
                password_hash=user.password_hash, role=user.role, 
                is_verified=user.is_verified, profile_pic_url=user.profile_pic_url, 
                bio=user.bio, created_at=user.created_at, uuid=user.uuid
            )
            new_db.add(new_user)
            new_db.flush()
            user_map[user.id] = new_user.id
        print(" Users migrated.")

        # C. Migrate Tags
        for tag in old_db.query(Tag).all():
            new_tag = Tag(name=tag.name, slug=tag.slug, uuid=tag.uuid)
            new_db.add(new_tag)
        new_db.flush()
        print("Tags migrated.")

        # D. Migrate Posts
        for post in old_db.query(Post).all():
            new_post = Post(
                title=post.title, content=post.content, slug=post.slug,
                author_id=user_map.get(post.author_id),
                category_id=category_map.get(post.category_id),
                status=post.status, created_at=post.created_at,
                uuid=post.uuid
            )
            new_db.add(new_post)
            new_db.flush()
            post_map[post.id] = new_post.id
        print("Posts migrated.")

        # E. Migrate Comments - NEW STEP
        for comment in old_db.query(Comment).all():
            new_comment = Comment(
                content=comment.content,
                # Map to new Post ID and new User ID
                post_id=post_map.get(comment.post_id),
                user_id=user_map.get(comment.user_id),
                created_at=comment.created_at,
                uuid=comment.uuid
            )
            new_db.add(new_comment)
        
        new_db.commit()
        print("--- SUCCESS: All data (including Comments) safely moved to Neon DB ---")

    except Exception as e:
        new_db.rollback()
        print(f" ERROR: {e}")
    finally:
        old_db.close()
        new_db.close()

if __name__ == "__main__":
    migrate()