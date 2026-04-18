-- ========================================
-- QUIZ GAME PLATFORM - DATABASE SCHEMA
-- ========================================
-- File: database/schema.sql

-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    total_games_played INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    profile_picture VARCHAR(255) DEFAULT 'default.png',
    status VARCHAR(10) DEFAULT 'active'
);

-- Create Categories Table
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(100) NOT NULL,
    category_description TEXT,
    category_image VARCHAR(255),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(10) DEFAULT 'active'
);

-- Create Questions Table
CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    question_text TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_answer CHAR(1) NOT NULL,
    difficulty_level VARCHAR(10) DEFAULT 'medium',
    points INTEGER DEFAULT 10,
    explanation TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(10) DEFAULT 'active',
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Create Game Sessions Table (Login Data)
CREATE TABLE IF NOT EXISTS game_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_end_time DATETIME,
    ip_address VARCHAR(45),
    device_type VARCHAR(50),
    browser_info VARCHAR(100),
    session_duration_minutes INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create Game Results Table (Each Game Played)
CREATE TABLE IF NOT EXISTS game_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_id INTEGER,
    category_id INTEGER,
    game_start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    game_end_time DATETIME,
    total_questions INTEGER DEFAULT 10,
    correct_answers INTEGER DEFAULT 0,
    wrong_answers INTEGER DEFAULT 0,
    score INTEGER DEFAULT 0,
    time_taken_seconds INTEGER DEFAULT 0,
    difficulty_level VARCHAR(10) DEFAULT 'medium',
    game_mode VARCHAR(50) DEFAULT 'standard',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (session_id) REFERENCES game_sessions(session_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Create User Answers Table (Track Every Answer)
CREATE TABLE IF NOT EXISTS user_answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_id INTEGER,
    question_id INTEGER,
    user_answer CHAR(1),
    is_correct BOOLEAN,
    time_taken_seconds INTEGER DEFAULT 0,
    answered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (result_id) REFERENCES game_results(result_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);

-- Create Feedback Table
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    rating INTEGER,
    comments TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);