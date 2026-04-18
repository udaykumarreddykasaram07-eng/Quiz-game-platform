# ========================================
# API ROUTES
# ========================================
# File: routes/api.py

from flask import Blueprint, jsonify, request, session
from models.user import User
from models.game import GameResult, Category, Question
from models.analytics import UserAnalytics

api_bp = Blueprint('api', __name__)

# ========================================
# PLATFORM STATISTICS
# ========================================

@api_bp.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall platform statistics"""
    try:
        total_users = User.query.count()
        total_questions = Question.query.count()
        total_games = GameResult.query.count()
        total_categories = Category.query.filter_by(status='active').count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_users': total_users,
                'total_questions': total_questions,
                'total_games': total_games,
                'total_categories': total_categories
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# USER STATISTICS
# ========================================

@api_bp.route('/api/user/stats', methods=['GET'])
def get_user_stats():
    """Get current user statistics"""
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'error': 'Not authenticated'
        }), 401
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get category-wise performance
        analytics = UserAnalytics.query.filter_by(user_id=user_id).all()
        category_performance = []
        
        for a in analytics:
            category_performance.append({
                'category_id': a.category_id,
                'category_name': a.category.category_name,
                'attempts': a.total_attempts,
                'correct': a.total_correct,
                'wrong': a.total_wrong,
                'accuracy': round(float(a.accuracy_percentage), 2),
                'average_time': a.average_time_per_question,
                'favorite': a.favorite_category
            })
        
        # Get recent games
        recent_games = GameResult.query.filter_by(user_id=user_id)\
            .order_by(GameResult.game_start_time.desc())\
            .limit(10).all()
        
        games_history = []
        for game in recent_games:
            games_history.append({
                'game_id': game.result_id,
                'category': game.category.category_name,
                'score': game.score,
                'correct': game.correct_answers,
                'wrong': game.wrong_answers,
                'total': game.total_questions,
                'date': game.game_start_time.isoformat()
            })
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'total_games': user.total_games_played,
                    'total_score': user.total_score,
                    'registration_date': user.registration_date.isoformat()
                },
                'category_performance': category_performance,
                'recent_games': games_history
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# LEADERBOARD API
# ========================================

@api_bp.route('/api/leaderboard', methods=['GET'])
def get_leaderboard_api():
    """Get leaderboard data"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        top_users = User.query.filter_by(status='active')\
            .order_by(User.total_score.desc())\
            .limit(limit).all()
        
        leaderboard = []
        for i, user in enumerate(top_users, 1):
            leaderboard.append({
                'rank': i,
                'user_id': user.user_id,
                'username': user.username,
                'total_score': user.total_score,
                'total_games': user.total_games_played,
                'average_score': round(user.total_score / user.total_games_played, 2) if user.total_games_played > 0 else 0
            })
        
        return jsonify({
            'success': True,
            'data': leaderboard
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# CATEGORIES API
# ========================================

@api_bp.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.filter_by(status='active').all()
        
        categories_list = []
        for c in categories:
            categories_list.append({
                'id': c.category_id,
                'name': c.category_name,
                'description': c.category_description,
                'image': c.category_image,
                'question_count': len(c.questions),
                'created_date': c.created_date.isoformat()
            })
        
        return jsonify({
            'success': True,
            'data': categories_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# USERNAME AVAILABILITY CHECK
# ========================================

@api_bp.route('/api/check-username', methods=['GET'])
def check_username():
    """Check if username is available"""
    try:
        username = request.args.get('username')
        
        if not username:
            return jsonify({
                'success': False,
                'available': False,
                'error': 'No username provided'
            }), 400
        
        # Check if username exists
        existing_user = User.query.filter_by(username=username).first()
        
        return jsonify({
            'success': True,
            'available': existing_user is None,
            'username': username
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# EMAIL AVAILABILITY CHECK
# ========================================

@api_bp.route('/api/check-email', methods=['GET'])
def check_email():
    """Check if email is available"""
    try:
        email = request.args.get('email')
        
        if not email:
            return jsonify({
                'success': False,
                'available': False,
                'error': 'No email provided'
            }), 400
        
        # Check if email exists
        existing_user = User.query.filter_by(email=email).first()
        
        return jsonify({
            'success': True,
            'available': existing_user is None,
            'email': email
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# QUESTION DETAILS API
# ========================================

@api_bp.route('/api/questions/<int:question_id>', methods=['GET'])
def get_question_details(question_id):
    """Get detailed information about a specific question"""
    try:
        question = Question.query.get_or_404(question_id)
        
        return jsonify({
            'success': True,
            'data': {
                'question_id': question.question_id,
                'category_id': question.category_id,
                'category_name': question.category.category_name,
                'question_text': question.question_text,
                'options': {
                    'A': question.option_a,
                    'B': question.option_b,
                    'C': question.option_c,
                    'D': question.option_d
                },
                'difficulty_level': question.difficulty_level,
                'points': question.points,
                'explanation': question.explanation
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# CATEGORY QUESTIONS COUNT
# ========================================

@api_bp.route('/api/categories/<int:category_id>/questions-count', methods=['GET'])
def get_category_questions_count(category_id):
    """Get the number of questions in a specific category"""
    try:
        count = Question.query.filter_by(
            category_id=category_id,
            status='active'
        ).count()
        
        category = Category.query.get(category_id)
        
        return jsonify({
            'success': True,
            'data': {
                'category_id': category_id,
                'category_name': category.category_name if category else 'Unknown',
                'questions_count': count
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# USER RANK API
# ========================================

@api_bp.route('/api/user/rank', methods=['GET'])
def get_user_rank():
    """Get current user's rank on leaderboard"""
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'error': 'Not authenticated'
        }), 401
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get all users ordered by score
        all_users = User.query.filter_by(status='active')\
            .order_by(User.total_score.desc())\
            .all()
        
        # Find user's rank
        rank = 1
        for u in all_users:
            if u.user_id == user_id:
                break
            rank += 1
        
        return jsonify({
            'success': True,
            'data': {
                'user_id': user_id,
                'username': user.username,
                'rank': rank,
                'total_users': len(all_users),
                'percentile': round((1 - (rank / len(all_users))) * 100, 2)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500