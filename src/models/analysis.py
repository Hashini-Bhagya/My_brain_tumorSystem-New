# In analysis.py
from datetime import datetime
from src.utils.db import db

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    image_url = db.Column(db.String(500), nullable=False)
    has_tumor = db.Column(db.Boolean, nullable=False)
    tumor_type = db.Column(db.String(50), nullable=True)  # glioma, meningioma, etc.
    confidence = db.Column(db.Float, nullable=False)
    tumor_probability = db.Column(db.Float, nullable=False)
    glioma_probability = db.Column(db.Float, default=0.0)
    meningioma_probability = db.Column(db.Float, default=0.0)
    notumor_probability = db.Column(db.Float, default=0.0)
    pituitary_probability = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    
#  relationship
    user = db.relationship("User", back_populates="analysis_results")

    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'has_tumor': self.has_tumor,
            'tumor_type': self.tumor_type,
            'confidence': self.confidence,
            'tumor_probability': self.tumor_probability,
            'probabilities': {
                'glioma': self.glioma_probability,
                'meningioma': self.meningioma_probability,
                'notumor': self.notumor_probability,
                'pituitary': self.pituitary_probability
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }