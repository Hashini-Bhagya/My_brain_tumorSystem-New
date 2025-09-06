from src.models.admin import Admin
from src.utils.db import db

def init_admin():
    """Initialize admin user if not exists"""
    # Check if admin table exists and has records
    if not Admin.query.first():
        admin = Admin(
            email="admin@braintumor.com",
            name="System Administrator"
        )
        admin.set_password("admin123")  # This will hash the password
        
        try:
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        except Exception as e:
            print(f"Error creating admin user: {str(e)}")
            db.session.rollback()