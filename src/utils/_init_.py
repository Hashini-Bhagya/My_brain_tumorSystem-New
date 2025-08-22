from flask import Flask
from flask_login import LoginManager
from config import Config
from src.utils.db import db, test_database_connection
from src.routes.api import api_bp
from src.routes.main_routes import main_bp
import os

login_manager = LoginManager()

def create_app():
    # Get the base directory of your project
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))
    
    app.config.from_object(Config)

    # Test DB connection
    if not test_database_connection():
        return None

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize login Manager
    login_manager.init_app(app)
    login_manager.login_view = "api.login"

    @login_manager.user_loader
    def load_user(user_id):
        from src.models.user import User
        return User.query.get(int(user_id))

    # Register Blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)  # main routes

    # Create DB tables inside app context
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")

    return app