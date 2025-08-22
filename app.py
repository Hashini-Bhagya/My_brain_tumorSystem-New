from flask import Flask
from config import Config
from src.utils.db import db, test_database_connection
from src.routes.api import api_bp
from src.routes.main_routes import main_bp
from flask_login import LoginManager
from src.utils._init_ import create_app

if __name__ == "__main__":
    app = create_app()
    if app:
        app.run(debug=True, host="0.0.0.0", port=5000)
