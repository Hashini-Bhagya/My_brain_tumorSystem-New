from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from mysql.connector import Error
from config import Config

db = SQLAlchemy()

def test_database_connection():
    try:

        from config import Config
        import mysql.connector
        
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        if conn.is_connected():
            print("✅ Successfully connected to MySQL database")
            conn.close()
            return True
    except Error as e:
        print(f"❌ Error connecting to MySQL database: {e}")
        return False
