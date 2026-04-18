from datetime import datetime
from flask_login import UserMixin
from extensions import db, bcrypt

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    total_games_played = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    profile_picture = db.Column(db.String(255), default='default.png')
    status = db.Column(db.String(10), default='active')
    
    game_sessions = db.relationship('GameSession', backref='user', lazy=True)
    game_results = db.relationship('GameResult', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.user_id)
    
    def update_stats(self, score):
        self.total_games_played += 1
        self.total_score += score
        self.last_login = datetime.utcnow()