# ========================================
# HELPER FUNCTIONS
# ========================================
# File: utils/helpers.py

from datetime import datetime, timedelta

def format_time(seconds):
    """Format seconds to MM:SS"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def calculate_accuracy(correct, total):
    """Calculate accuracy percentage"""
    if total == 0:
        return 0.0
    return (correct / total) * 100

def get_grade(score):
    """Get grade based on score"""
    if score >= 90:
        return 'A+'
    elif score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    elif score >= 50:
        return 'D'
    else:
        return 'F'

def time_ago(dt):
    """Get human-readable time ago"""
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 365:
        return f"{diff.days // 365} years ago"
    elif diff.days > 30:
        return f"{diff.days // 30} months ago"
    elif diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600} hours ago"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60} minutes ago"
    else:
        return "just now"