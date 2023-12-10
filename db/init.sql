---- Create a new user
--CREATE USER 'root'@'root' IDENTIFIED BY 'user_password';
--
--CREATE DATABASE digit;
--
---- Grant privileges to the user on the database
--GRANT ALL PRIVILEGES ON digit.* TO 'root'@'root';
--
---- Connect to the new database
--USE digit;
---- Create a new table
--CREATE TABLE classification_data (
--    id SERIAL PRIMARY KEY,
--    image BYTEA,
--    prediction VARCHAR(1)
--);

---- Create a new user
--CREATE USER 'root'@'root' IDENTIFIED BY 'user_password';

-- Create the digit database
CREATE DATABASE IF NOT EXISTS digit;


---- Grant privileges to the user on the digit database
--GRANT ALL PRIVILEGES ON digit.* TO 'root'@'root';

-- Switch to the digit database
USE digit;

-- Create a new table
CREATE TABLE classification_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image LONGBLOB,
    prediction VARCHAR(1)
);

