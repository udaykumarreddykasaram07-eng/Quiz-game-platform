# ========================================
# QUIZ GAME PLATFORM - MAIN APPLICATION
# ========================================
# File: app.py

from flask import Flask, render_template, redirect, url_for, flash, session
from datetime import timedelta
import os

# Import extensions (avoids circular imports)
from extensions import db, bcrypt, login_manager

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production-1234567890'

# Database configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'quiz_game.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Initialize extensions with app
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# ========================================
# IMPORT MODELS (after extensions initialized)
# ========================================
from models.user import User
from models.game import GameSession, GameResult, UserAnswer, Category, Question
from models.analytics import UserAnalytics, Feedback

# ========================================
# LOGIN MANAGER CONFIGURATION
# ========================================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ========================================
# IMPORT AND REGISTER ROUTES (after models)
# ========================================
from routes.auth import auth_bp
from routes.game import game_bp
from routes.api import api_bp

app.register_blueprint(auth_bp)
app.register_blueprint(game_bp, url_prefix='/game')
app.register_blueprint(api_bp, url_prefix='/api')

# Debug routes (development only)
if app.debug:
    from routes.debug import debug_bp
    app.register_blueprint(debug_bp, url_prefix='/debug')

# ========================================
# ERROR HANDLERS
# ========================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(401)
def unauthorized(e):
    flash('You need to login to access this page', 'info')
    return redirect(url_for('auth.login'))

# ========================================
# MAIN ROUTES
# ========================================
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('game.dashboard'))
    return render_template('index.html')

@app.route('/test-db')
def test_db():
    try:
        from database.connection import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM questions")
        questions = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM categories")
        categories = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM users")
        users = cursor.fetchone()['count']
        conn.close()
        
        game_results = GameResult.query.count()
        game_sessions = GameSession.query.count()
        
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 30px; background: #f0f9ff; border-radius: 10px;">
            <h1 style="color: #6366f1; text-align: center;">✅ Database Connected Successfully!</h1>
            <hr style="margin: 30px 0;">
            <h2 style="color: #1e293b;">📊 Statistics:</h2>
            <ul style="font-size: 18px; line-height: 2;">
                <li><strong>Questions:</strong> {questions}</li>
                <li><strong>Categories:</strong> {categories}</li>
                <li><strong>Users:</strong> {users}</li>
                <li><strong>Game Results:</strong> {game_results}</li>
                <li><strong>Sessions:</strong> {game_sessions}</li>
            </ul>
        </div>
        """
    except Exception as e:
        return f"<h2 style='color:red'>❌ Database Error: {str(e)}</h2>"

# ========================================
# START APPLICATION
# ========================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', full_name='Admin User')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin created: username='admin', password='admin123'")
    
    print("\n" + "="*60)
    print("🎮 QUIZ GAME PLATFORM - READY!")
    print("="*60)
    print(f"🚀 Running on http://localhost:5002")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5004)