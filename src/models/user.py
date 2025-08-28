from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#db = SQLAlchemy()

from src.utils.db import db

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
   # password_hash = db.Column(db.String(255), nullable=False)
   # Modify password_hash to allow NULL for OAuth users
    password_hash = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())
    
    # Add relationship to AnalysisResult
    analyses = db.relationship('AnalysisResult', backref='users', lazy=True)

    analysis_results = db.relationship("AnalysisResult", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

   # def check_password(self, password):
       # return check_password_hash(self.password_hash, password)
    
    #for google auth
    def check_password(self, password):
        if self.password_hash is None:
            # For OAuth users who don't have a password
            return False
        return check_password_hash(self.password_hash, password) 
    
    def get_id(self) -> str:
        # ✅ typed session id
        return f"user:{self.id}"