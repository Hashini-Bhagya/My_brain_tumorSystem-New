from src.models.user import User #new
from src.utils.db import db #new
from src.models.user import User, db
from flask_login import login_user

class UserController:
    @staticmethod
    def create_user(user_data):
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                return None, "User with this email already exists"
            
            # Create new user
            new_user = User(
                name=user_data['name'],
                email=user_data['email'],
                address=user_data.get('address'),
                age=user_data.get('age'),
                gender=user_data.get('gender')
            )
            new_user.set_password(user_data['password'])
            
            db.session.add(new_user)
            db.session.commit()
            
            return new_user, "User created successfully"
            
        except Exception as e:
            db.session.rollback()
            return None, f"Error creating user: {str(e)}"
    
    @staticmethod
    def authenticate_user(email, password):
        try:
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                return user, "Login successful"
            return None, "Invalid email or password"
        except Exception as e:
            return None, f"Error during authentication: {str(e)}"
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)