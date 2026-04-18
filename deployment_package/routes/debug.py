# ========================================
# DEBUG & TESTING ROUTES
# ========================================
# File: routes/debug.py

from flask import Blueprint, render_template, jsonify, request
from app import db
from models.user import User
from models.game import GameResult, Category, Question, GameSession
from models.analytics import UserAnalytics, Feedback
from datetime import datetime

debug_bp = Blueprint('debug', __name__)

# ========================================
# DATABASE STATS
# ========================================

@debug_bp.route('/debug/stats')
def debug_stats():
    """Show database statistics"""
    stats = {
        'users': User.query.count(),
        'game_sessions': GameSession.query.count(),
        'game_results': GameResult.query.count(),
        'categories': Category.query.count(),
        'questions': Question.query.count(),
        'user_analytics': UserAnalytics.query.count(),
        'feedback': Feedback.query.count()
    }
    
    return jsonify({
        'success': True,
        'timestamp': datetime.now().isoformat(),
        'stats': stats
    })

# ========================================
# TEST USER CREATION
# ========================================

@debug_bp.route('/debug/create-test-user', methods=['POST'])
def create_test_user():
    """Create a test user for debugging"""
    try:
        data = request.get_json() or {}
        username = data.get('username', f'testuser_{datetime.now().timestamp()}')
        email = data.get('email', f'{username}@test.com')
        password = data.get('password', 'test123')
        full_name = data.get('full_name', 'Test User')
        
        # Check if user exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            return jsonify({
                'success': False,
                'error': 'User already exists'
            }), 400
        
        # Create user
        user = User(
            username=username,
            email=email,
            full_name=full_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Test user created successfully',
            'user': {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# CLEAR TEST DATA
# ========================================

@debug_bp.route('/debug/clear-test-data', methods=['POST'])
def clear_test_data():
    """Clear test data (keep admin user)"""
    try:
        # Delete all game results and related data
        GameResult.query.delete()
        GameSession.query.delete()
        UserAnalytics.query.delete()
        Feedback.query.delete()
        
        # Delete all users except admin
        User.query.filter(User.username != 'admin').delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Test data cleared successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# DATABASE INTEGRITY CHECK
# ========================================

@debug_bp.route('/debug/check-integrity')
def check_integrity():
    """Check database integrity"""
    issues = []
    
    # Check for orphaned game results
    orphaned_results = db.session.execute("""
        SELECT COUNT(*) as count FROM game_results 
        WHERE user_id NOT IN (SELECT user_id FROM users)
    """).fetchone()
    
    if orphaned_results['count'] > 0:
        issues.append(f'Found {orphaned_results["count"]} orphaned game results')
    
    # Check for orphaned user answers
    orphaned_answers = db.session.execute("""
        SELECT COUNT(*) as count FROM user_answers 
        WHERE result_id NOT IN (SELECT result_id FROM game_results)
    """).fetchone()
    
    if orphaned_answers['count'] > 0:
        issues.append(f'Found {orphaned_answers["count"]} orphaned user answers')
    
    # Check for categories with no questions
    empty_categories = db.session.execute("""
        SELECT c.category_name FROM categories c
        LEFT JOIN questions q ON c.category_id = q.category_id
        WHERE q.question_id IS NULL AND c.status = 'active'
    """).fetchall()
    
    if empty_categories:
        issues.append(f'Found {len(empty_categories)} categories with no questions')
    
    return jsonify({
        'success': len(issues) == 0,
        'issues': issues,
        'message': 'No issues found' if len(issues) == 0 else f'Found {len(issues)} issues'
    })

# ========================================
# PERFORMANCE METRICS
# ========================================

@debug_bp.route('/debug/performance')
def performance_metrics():
    """Get performance metrics"""
    from sqlalchemy import func
    
    # Average game duration
    avg_duration = db.session.query(func.avg(GameResult.time_taken_seconds)).scalar() or 0
    
    # Average score
    avg_score = db.session.query(func.avg(GameResult.score)).scalar() or 0
    
    # Most popular category
    popular_category = db.session.query(
        Category.category_name,
        func.count(GameResult.result_id).label('count')
    ).join(GameResult).group_by(Category.category_id)\
     .order_by(func.count(GameResult.result_id).desc()).first()
    
    # Average accuracy
    avg_accuracy = db.session.query(
        func.avg(UserAnalytics.accuracy_percentage)
    ).scalar() or 0
    
    return jsonify({
        'success': True,
        'metrics': {
            'average_game_duration_seconds': round(avg_duration, 2),
            'average_score': round(avg_score, 2),
            'most_popular_category': popular_category[0] if popular_category else 'N/A',
            'average_accuracy_percentage': round(avg_accuracy, 2),
            'total_games_played': GameResult.query.count(),
            'total_users': User.query.count()
        }
    })

# ========================================
# EXPORT DATABASE (for backup)
# ========================================

@debug_bp.route('/debug/export')
def export_database():
    """Export database summary (not full dump)"""
    summary = {
        'users': [u.username for u in User.query.all()],
        'categories': [c.category_name for c in Category.query.all()],
        'total_questions': Question.query.count(),
        'total_games': GameResult.query.count(),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'export': summary
    })