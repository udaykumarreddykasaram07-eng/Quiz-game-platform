from datetime import datetime
from extensions import db

class GameSession(db.Model):
    __tablename__ = 'game_sessions'
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    session_start_time = db.Column(db.DateTime, default=datetime.utcnow)
    session_end_time = db.Column(db.DateTime)
    ip_address = db.Column(db.String(45))
    device_type = db.Column(db.String(50))
    browser_info = db.Column(db.String(100))
    session_duration_minutes = db.Column(db.Integer, default=0)
    game_results = db.relationship('GameResult', backref='session', lazy=True)

class GameResult(db.Model):
    __tablename__ = 'game_results'
    result_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('game_sessions.session_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    game_start_time = db.Column(db.DateTime, default=datetime.utcnow)
    game_end_time = db.Column(db.DateTime)
    total_questions = db.Column(db.Integer, default=10)
    correct_answers = db.Column(db.Integer, default=0)
    wrong_answers = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)
    time_taken_seconds = db.Column(db.Integer, default=0)
    difficulty_level = db.Column(db.String(10), default='medium')
    game_mode = db.Column(db.String(50), default='standard')
    user_answers = db.relationship('UserAnswer', backref='game_result', lazy=True, cascade='all, delete-orphan')

class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    answer_id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('game_results.result_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    user_answer = db.Column(db.String(1))
    is_correct = db.Column(db.Boolean)
    time_taken_seconds = db.Column(db.Integer, default=0)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
    question = db.relationship('Question', backref='user_answers', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    category_description = db.Column(db.Text)
    category_image = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10), default='active')
    questions = db.relationship('Question', backref='category', lazy=True)
    game_results = db.relationship('GameResult', backref='category', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)
    difficulty_level = db.Column(db.String(10), default='medium')
    points = db.Column(db.Integer, default=10)
    explanation = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10), default='active')