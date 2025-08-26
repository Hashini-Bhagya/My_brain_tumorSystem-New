from flask import Flask, request, jsonify
from config import Config
from src.utils.db import db, test_database_connection
from src.routes.api import api_bp
from src.routes.main_routes import main_bp
from flask_login import LoginManager
from src.utils._init_ import create_app
import os
from dotenv import load_dotenv

load_dotenv()

# Add this debug section
def check_google_config():
    print("=== GOOGLE OAUTH CONFIGURATION CHECK ===")
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    print(f"CLIENT_ID: {client_id}")
    print(f"CLIENT_ID valid: {bool(client_id and client_id != '441128910074-fpqe3k8eo6i8g54rcfp2c12eisrq6ssc.apps.googleusercontent.com')}")
    print(f"CLIENT_SECRET: {'*' * len(client_secret) if client_secret else 'MISSING'}")
    print(f"CLIENT_SECRET valid: {bool(client_secret and client_secret != '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')}")
    
    # Check if .env file exists and is readable
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    print(f".env file exists: {os.path.exists(env_path)}")
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            content = f.read()
            print(".env content:")
            for line in content.split('\n'):
                if 'GOOGLE' in line and 'SECRET' not in line:
                    print(f"  {line}")
                elif 'SECRET' in line:
                    print(f"  GOOGLE_CLIENT_SECRET=******")

check_google_config()

if __name__ == "__main__":
    app = create_app()
    if app:
        app.run(debug=True, host="0.0.0.0", port=5000)
