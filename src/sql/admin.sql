-- Create database for brain tumor detection system
CREATE DATABASE IF NOT EXISTS brain_tumor_db;
USE brain_tumor_db;

-- Create admin table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert default admin user (password: admin123)
INSERT INTO admins (email, password_hash, name)
VALUES ('admin@braintumor.com', '$2b$12$rG.5VUu6p.7QdKc9jZxYPeOcWQ1W2sR3T4U5V6W7X8Y9Z0A1B2C3D', 'System Administrator');

-- Show tables to verify
SHOW TABLES;