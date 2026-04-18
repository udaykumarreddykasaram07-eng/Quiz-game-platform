# ========================================
# TEST DATA GENERATOR
# ========================================
# File: test_data.py

import sqlite3
import os
from datetime import datetime, timedelta
import random

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'quiz_game.db')

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_test_users():
    """Generate test users"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    test_users = [
        ('john_doe', 'john@example.com', 'John Doe'),
        ('jane_smith', 'jane@example.com', 'Jane Smith'),
        ('alex_wilson', 'alex@example.com', 'Alex Wilson'),
        ('sarah_jones', 'sarah@example.com', 'Sarah Jones'),
        ('mike_brown', 'mike@example.com', 'Mike Brown'),
        ('emily_davis', 'emily@example.com', 'Emily Davis'),
        ('david_miller', 'david@example.com', 'David Miller'),
        ('lisa_taylor', 'lisa@example.com', 'Lisa Taylor'),
        ('kevin_white', 'kevin@example.com', 'Kevin White'),
        ('amanda_clark', 'amanda@example.com', 'Amanda Clark')
    ]
    
    for username, email, full_name in test_users:
        # Check if user exists
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            continue
        
        # Insert user with hashed password (password = username)
        password_hash = f"pbkdf2:sha256:150000${username}hash"  # Simplified for testing
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name, registration_date, total_games_played, total_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, email, password_hash, full_name, 
              datetime.now() - timedelta(days=random.randint(1, 30)),
              random.randint(5, 50),
              random.randint(100, 5000)))
    
    conn.commit()
    print(f"✓ Generated {len(test_users)} test users")
    conn.close()

def generate_test_game_sessions():
    """Generate test game sessions"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    for user in users:
        user_id = user['user_id']
        
        # Generate 1-5 sessions per user
        num_sessions = random.randint(1, 5)
        
        for i in range(num_sessions):
            start_time = datetime.now() - timedelta(days=random.randint(0, 30))
            end_time = start_time + timedelta(minutes=random.randint(5, 60))
            
            cursor.execute("""
                INSERT INTO game_sessions (user_id, session_start_time, session_end_time, ip_address, device_type, browser_info, session_duration_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, start_time, end_time,
                  f"192.168.1.{random.randint(1, 254)}",
                  random.choice(['Desktop', 'Mobile', 'Tablet']),
                  random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
                  (end_time - start_time).seconds // 60))
    
    conn.commit()
    print(f"✓ Generated game sessions for {len(users)} users")
    conn.close()

def generate_test_game_results():
    """Generate test game results"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all users and categories
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    cursor.execute("SELECT category_id FROM categories")
    categories = cursor.fetchall()
    
    for user in users:
        user_id = user['user_id']
        
        # Get user's sessions
        cursor.execute("SELECT session_id FROM game_sessions WHERE user_id = ?", (user_id,))
        sessions = cursor.fetchall()
        
        if not sessions:
            continue
        
        # Generate 3-10 game results per user
        num_games = random.randint(3, 10)
        
        for i in range(num_games):
            session_id = random.choice(sessions)['session_id']
            category_id = random.choice(categories)['category_id']
            
            total_questions = 10
            correct_answers = random.randint(3, 10)
            wrong_answers = total_questions - correct_answers
            
            # Calculate score based on difficulty
            difficulty = random.choice(['easy', 'medium', 'hard'])
            if difficulty == 'easy':
                base_points = 10
            elif difficulty == 'medium':
                base_points = 15
            else:
                base_points = 20
            
            score = correct_answers * base_points
            
            start_time = datetime.now() - timedelta(days=random.randint(0, 30))
            end_time = start_time + timedelta(seconds=random.randint(60, 600))
            
            cursor.execute("""
                INSERT INTO game_results 
                (user_id, session_id, category_id, game_start_time, game_end_time, 
                 total_questions, correct_answers, wrong_answers, score, time_taken_seconds, 
                 difficulty_level, game_mode)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, session_id, category_id, start_time, end_time,
                  total_questions, correct_answers, wrong_answers, score,
                  (end_time - start_time).seconds, difficulty, 'standard'))
    
    conn.commit()
    print(f"✓ Generated game results for {len(users)} users")
    conn.close()

def generate_test_user_answers():
    """Generate test user answers"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all game results
    cursor.execute("SELECT result_id, category_id FROM game_results")
    game_results = cursor.fetchall()
    
    for result in game_results:
        result_id = result['result_id']
        category_id = result['category_id']
        
        # Get 10 random questions from this category
        cursor.execute("""
            SELECT question_id, correct_answer FROM questions 
            WHERE category_id = ? AND status = 'active' 
            ORDER BY RANDOM() LIMIT 10
        """, (category_id,))
        questions = cursor.fetchall()
        
        for question in questions:
            question_id = question['question_id']
            correct_answer = question['correct_answer']
            
            # 70% chance of correct answer
            is_correct = random.random() < 0.7
            user_answer = correct_answer if is_correct else random.choice(['A', 'B', 'C', 'D'])
            
            cursor.execute("""
                INSERT INTO user_answers (result_id, question_id, user_answer, is_correct, time_taken_seconds, answered_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (result_id, question_id, user_answer, is_correct,
                  random.randint(5, 30),
                  datetime.now() - timedelta(seconds=random.randint(0, 3600))))
    
    conn.commit()
    print(f"✓ Generated user answers for {len(game_results)} games")
    conn.close()

def generate_test_analytics():
    """Generate test user analytics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all users and categories
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    cursor.execute("SELECT category_id FROM categories")
    categories = cursor.fetchall()
    
    for user in users:
        user_id = user['user_id']
        
        # Pick 2-4 favorite categories per user
        num_categories = random.randint(2, 4)
        selected_categories = random.sample(categories, num_categories)
        
        for i, category in enumerate(selected_categories):
            category_id = category['category_id']
            
            total_attempts = random.randint(5, 20)
            total_correct = random.randint(3, total_attempts)
            total_wrong = total_attempts - total_correct
            
            accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
            
            cursor.execute("""
                INSERT INTO user_analytics 
                (user_id, category_id, total_attempts, total_correct, total_wrong, 
                 accuracy_percentage, average_time_per_question, favorite_category, last_played)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, category_id, total_attempts, total_correct, total_wrong,
                  round(accuracy, 2),
                  random.randint(10, 30),
                  i == 0,  # First category is favorite
                  datetime.now() - timedelta(days=random.randint(0, 30))))
    
    conn.commit()
    print(f"✓ Generated analytics for {len(users)} users")
    conn.close()

def generate_all_test_data():
    """Generate all test data"""
    print("\n" + "="*50)
    print("GENERATING TEST DATA")
    print("="*50 + "\n")
    
    try:
        generate_test_users()
        generate_test_game_sessions()
        generate_test_game_results()
        generate_test_user_answers()
        generate_test_analytics()
        
        print("\n" + "="*50)
        print("✓ ALL TEST DATA GENERATED SUCCESSFULLY!")
        print("="*50 + "\n")
        
        # Show summary
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM users")
        users_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM game_results")
        games_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM user_answers")
        answers_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM user_analytics")
        analytics_count = cursor.fetchone()['count']
        
        conn.close()
        
        print("📊 DATABASE SUMMARY:")
        print(f"   • Users: {users_count}")
        print(f"   • Games Played: {games_count}")
        print(f"   • Answers Recorded: {answers_count}")
        print(f"   • Analytics Records: {analytics_count}")
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"\n✗ Error generating test data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    generate_all_test_data()