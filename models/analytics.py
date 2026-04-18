# ========================================
# ANALYTICS MODELS
# ========================================
# File: models/analytics.py

from datetime import datetime
from extensions import db

class UserAnalytics(db.Model):
    __tablename__ = 'user_analytics'
    
    analytics_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    total_attempts = db.Column(db.Integer, default=0, nullable=False)
    total_correct = db.Column(db.Integer, default=0, nullable=False)
    total_wrong = db.Column(db.Integer, default=0, nullable=False)
    accuracy_percentage = db.Column(db.Numeric(5, 2), default=0.00, nullable=False)
    average_time_per_question = db.Column(db.Integer, default=0, nullable=False)
    favorite_category = db.Column(db.Boolean, default=False)
    last_played = db.Column(db.DateTime)
    
    user = db.relationship('User', backref='analytics', lazy=True)
    category = db.relationship('Category', backref='analytics', lazy=True)
    
    def __init__(self, **kwargs):
        """Initialize with default values to prevent NoneType errors"""
        super(UserAnalytics, self).__init__(**kwargs)
        # Ensure all numeric fields have default values
        if self.total_attempts is None:
            self.total_attempts = 0
        if self.total_correct is None:
            self.total_correct = 0
        if self.total_wrong is None:
            self.total_wrong = 0
        if self.accuracy_percentage is None:
            self.accuracy_percentage = 0.00
        if self.average_time_per_question is None:
            self.average_time_per_question = 0
    
    def update_stats(self, correct, wrong, time_taken):
        """Update analytics after each game"""
        # Ensure values are not None before updating
        if self.total_attempts is None:
            self.total_attempts = 0
        if self.total_correct is None:
            self.total_correct = 0
        if self.total_wrong is None:
            self.total_wrong = 0
        
        self.total_attempts += 1
        self.total_correct += correct
        self.total_wrong += wrong
        self.last_played = datetime.utcnow()
        
        # Calculate accuracy
        total = self.total_correct + self.total_wrong
        if total > 0:
            self.accuracy_percentage = (self.total_correct / total) * 100
        else:
            self.accuracy_percentage = 0.00
        
        # Calculate average time
        if self.total_attempts > 0:
            self.average_time_per_question = time_taken // self.total_attempts
        else:
            self.average_time_per_question = 0

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    feedback_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)