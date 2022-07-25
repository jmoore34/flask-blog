-- Active: 1658474478161@@127.0.0.1@3306
DROP TABLE IF EXISTS messages;

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(25) UNIQUE NOT NULL,
    email VARCHAR(25) UNIQUE NOT NULL,
    password_hash CHAR(60) NOT NULL,
    is_admin BOOLEAN NOT NULL CHECK (is_admin IN (0,1)) DEFAULT 0
);

-- Insert admin user
INSERT INTO users (username, email, password_hash, is_admin) VALUES
("admin", "admin@smoothstack.com", "$2b$12$ZeboAFxNgixhWn5PztL2CuUwXMgf.UcupLwipqpJWruQwlcyRNlty", 1);