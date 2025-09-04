from src.utils.db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                          onupdate=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        # ✅ typed session id
        return f"admin:{self.id}"

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    #for mg 

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Enum('new', 'read', 'replied'), default='new', nullable=False)  # Added nullable=False
    replies = db.relationship('MessageReply', backref='message', lazy=True)

    # ADD THIS CONSTRUCTOR METHOD:
    def __init__(self, name=None, email=None, subject=None, message=None, status='new'):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        self.status = status

class MessageReply(db.Model):
    __tablename__ = 'message_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    reply_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    #admins = db.relationship('Admins', foreign_keys=[admins_id], backref='replies')

    admin = db.relationship('Admin', backref='replies')

def get_all_messages(cls):
    return db.session.query(Message).order_by(Message.created_at.desc()).all()

def get_message_by_id(cls, message_id):
    return Message.query.get(message_id)

@classmethod
def add_reply_to_message(cls, message_id, admin_id, reply_text):
        try:
            from . import MessageReply, Message
            
            # Create the reply
            reply = MessageReply(
                message_id=message_id,
                admin_id=admin_id,
                reply_text=reply_text
            )
            
            db.session.add(reply)
            
            # Update message status to 'replied'
            message = Message.query.get(message_id)
            if message:
                message.status = 'replied'
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error adding reply: {e}")
            import traceback
            traceback.print_exc()
            return False