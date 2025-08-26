import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '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'
    
    # MySQL Database configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'root'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'brain_tumor_db'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)

    # Flask configuration --- aluthen danne 
    #SECRET_KEY = os.environ.get('SECRET_KEY', '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')
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # Cloudinary configuration
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME') or 'dtz3ihwo2'
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY') or '445723323224991'
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') or 'dyaqAdlHIf9jZufLgpY4Xv38xxg'

    # Gemini AI configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

    #for google auth
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

    
    # Debug configuration
    DEBUG = True

# Add this to verify configuration
def check_config():
    print("=== CONFIGURATION CHECK ===")
    print(f"GOOGLE_CLIENT_ID: {Config.GOOGLE_CLIENT_ID}")
    print(f"GOOGLE_CLIENT_SECRET: {'*' * len(Config.GOOGLE_CLIENT_SECRET) if Config.GOOGLE_CLIENT_SECRET else 'MISSING'}")
    
    # Check if .env file exists
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    print(f".env file exists: {os.path.exists(env_path)}")
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            content = f.read()
            print(".env content preview:")
            for line in content.split('\n'):
                if 'GOOGLE' in line:
                    print(f"  {line}")

# Run the check when this module is imported
check_config()