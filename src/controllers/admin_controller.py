from src.models.admin import Admin
from src.models.user import User
from src.models.analysis import AnalysisResult
from src.utils.db import db
from flask_login import login_user as flask_login_user
from werkzeug.security import check_password_hash

class AdminController:
    
    @staticmethod
    def authenticate_admin(email, password):
        """Authenticate admin user"""
        admin = Admin.query.filter_by(email=email, is_active=True).first()
        if admin and admin.check_password(password):
            return admin, "Login successful"
        return None, "Invalid email or password"
    
    @staticmethod
    def get_all_users():
        """Get all users with their analysis count"""
        users = User.query.all()
        result = []
        for user in users:
            analysis_count = AnalysisResult.query.filter_by(user_id=user.id).count()
            result.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'address': user.address,
                'age': user.age,
                'gender': user.gender,
                'created_at': user.created_at,
                'analysis_count': analysis_count
            })
        return result
    
    @staticmethod
    def get_all_analyses():
        """Get all analysis results with user information"""
        analyses = AnalysisResult.query.join(User).all()
        result = []
        for analysis in analyses:
            result.append({
                'id': analysis.id,
                'user_id': analysis.user_id,
                'user_name': analysis.user.name,
                'user_email': analysis.user.email,
                'image_url': analysis.image_url,
                'has_tumor': analysis.has_tumor,
                'tumor_type': analysis.tumor_type,
                'confidence': analysis.confidence,
                'tumor_probability': analysis.tumor_probability,
                'glioma_probability': analysis.glioma_probability,
                'meningioma_probability': analysis.meningioma_probability,
                'notumor_probability': analysis.notumor_probability,
                'pituitary_probability': analysis.pituitary_probability,
                'created_at': analysis.created_at
            })
        return result
    
    @staticmethod
    def get_users_with_report_breakdown():
        """Return users with breakdown of how many reports of each type they have"""
        users = User.query.all()
        result = []

        for user in users:
            reports = {
                "glioma": 0,
                "meningioma": 0,
                "pituitary": 0,
                "notumor": 0
            }

            for analysis in user.analyses:
                if analysis.tumor_type in reports:
                    reports[analysis.tumor_type] += 1

            result.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "total_reports": len(user.analyses),
                "report_breakdown": reports
            })
        return result

    