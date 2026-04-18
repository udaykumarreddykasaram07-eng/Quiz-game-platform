# ========================================
# DATABASE CONNECTION
# ========================================
# File: database/connection.py

import sqlite3
import os

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'quiz_game.db')

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def init_database():
    """Initialize the database with schema and sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Read and execute schema
    schema_file = os.path.join(BASE_DIR, 'schema.sql')
    with open(schema_file, 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    # Read and execute sample data
    data_file = os.path.join(BASE_DIR, 'sample_data.sql')
    with open(data_file, 'r') as f:
        data = f.read()
        cursor.executescript(data)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()