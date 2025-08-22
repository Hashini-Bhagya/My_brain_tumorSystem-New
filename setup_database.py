# setup_database.py
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    try:
        print("Attempting to connect to MySQL...")
        
        # Get environment variables with fallback values
        host = os.environ.get('MYSQL_HOST', 'localhost')
        user = os.environ.get('MYSQL_USER', 'root')
        password = os.environ.get('MYSQL_PASSWORD', '')
        port = int(os.environ.get('MYSQL_PORT', '3306'))
        db_name = os.environ.get('MYSQL_DB', 'brain_tumor_db')
        
        print(f"Connecting to MySQL with: user={user}, host={host}, port={port}")
        
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✓ Database '{db_name}' created successfully")
        
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
        print("✓ Users table created successfully")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Database setup completed successfully!")
        return True
        
    except Error as e:
        print(f"✗ Error setting up database: {e}")
        print("Please check:")
        print("1. Is MySQL running?")
        print("2. Are your MySQL credentials correct in the .env file?")
        print("3. Try connecting with: mysql -u root -p")
        return False

if __name__ == '__main__':
    setup_database()