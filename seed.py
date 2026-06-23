from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.post import Category
from app.core.security import get_password_hash
from app.Services.post_service import slugify

def seed():
    print(" Initializing Database...")
    # This creates tables if they don't exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Seed Admin
        admin_email = "admin@mithilaroots.com"
        # Check if user exists
        admin_user = db.query(User).filter(User.email == admin_email).first()
        
        if not admin_user:
            admin = User(
                username="admin_official",
                email=admin_email,
                password_hash=get_password_hash("Admin123!"), 
                role=UserRole.ADMIN,  # Using the Enum correctly
                is_verified=True,
                bio="Official Administrator"
            )
            db.add(admin)
            print(" Admin user created.")
        else:
            print(" Admin user already exists.")

        # 2. Seed Default Categories
        categories = ["Technology", "Programming", "Lifestyle", "Business"]
        
        
        for cat_name in categories:
            slug = slugify(cat_name)
            if not db.query(Category).filter(Category.slug == slug).first():
                db.add(Category(name=cat_name, slug=slug))
                print(f" Category '{cat_name}' added.")
        
        db.commit()
        print(" Seeding completed successfully.")
        
    except Exception as e:
        print(f" Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()