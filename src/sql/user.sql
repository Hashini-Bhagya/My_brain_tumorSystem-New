-- Create database for brain tumor detection system
CREATE DATABASE IF NOT EXISTS brain_tumor_db;
USE brain_tumor_db;

-- Users table for registration
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
);

--- analysis_result table ------
CREATE TABLE analysis_result (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    has_tumor BOOLEAN NOT NULL,
    tumor_type VARCHAR(50),
    confidence FLOAT NOT NULL,
    tumor_probability FLOAT NOT NULL,
    glioma_probability FLOAT DEFAULT 0.0,
    meningioma_probability FLOAT DEFAULT 0.0,
    notumor_probability FLOAT DEFAULT 0.0,
    pituitary_probability FLOAT DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)  -- Changed from user(id) to users(id)
);

SHOW TABLES;   