# setup_database.py
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST') or 'localhost',
            user=os.environ.get('MYSQL_USER') or 'root',
            password=os.environ.get('MYSQL_PASSWORD') or '',
            port=int(os.environ.get('MYSQL_PORT') or 3306)
        )
        
        cursor = conn.cursor()
        
        # Create database
        db_name = os.environ.get('MYSQL_DB') or 'brain_tumor_db'
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created successfully")
        
        # Use the database
        cursor.execute(f"USE {db_name}")
        
        # Create users table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            address TEXT,
            age INT,
            gender ENUM('Male', 'Female', 'Other'),
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_sql)
        print("Users table created successfully")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Database setup completed successfully!")
        return True
        
    except Error as e:
        print(f"Error setting up database: {e}")
        print("Please check your MySQL credentials in the .env file")
        return False

if __name__ == '__main__':
    setup_database()