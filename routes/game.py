# ========================================
# GAME ROUTES
# ========================================
# File: routes/game.py

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime
import random
from extensions import db

game_bp = Blueprint('game', __name__)

# ========================================
# DASHBOARD ROUTE
# ========================================
@game_bp.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from models.user import User
    from models.game import GameResult, Category
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    recent_results = GameResult.query.filter_by(user_id=user_id)\
        .order_by(GameResult.game_start_time.desc())\
        .limit(5).all()
    
    categories = Category.query.filter_by(status='active').all()
    
    return render_template('dashboard.html', 
                         user=user, 
                         recent_results=recent_results,
                         categories=categories)

# ========================================
# QUIZ SELECTION ROUTE
# ========================================
@game_bp.route('/quiz')
def quiz():
    """Quiz selection page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from models.game import Category
    
    categories = Category.query.filter_by(status='active').all()
    return render_template('quiz.html', categories=categories)

# ========================================
# PLAY QUIZ ROUTE
# ========================================
@game_bp.route('/play/<int:category_id>')
def play_quiz(category_id):
    """Play quiz page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from models.game import Category, Question
    
    category = Category.query.get_or_404(category_id)
    
    questions = Question.query.filter_by(
        category_id=category_id, 
        status='active'
    ).order_by(db.func.random()).limit(10).all()
    
    if len(questions) < 10:
        flash('Not enough questions in this category', 'error')
        return redirect(url_for('game.quiz'))
    
    session['quiz_questions'] = [q.question_id for q in questions]
    session['quiz_category'] = category_id
    session['quiz_start_time'] = datetime.utcnow().isoformat()
    
    return render_template('play.html', 
                         category=category.category_name, 
                         questions=questions,
                         category_id=category_id)

# ========================================
# SUBMIT QUIZ ROUTE
# ========================================
@game_bp.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    """Submit quiz answers and calculate score"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from models.game import GameResult, UserAnswer, Question, Category
    from models.user import User
    from models.analytics import UserAnalytics
    
    user_id = session['user_id']
    category_id = int(request.form.get('category_id'))
    questions = session.get('quiz_questions', [])
    
    if not questions:
        flash('Quiz session expired. Please start again.', 'error')
        return redirect(url_for('game.quiz'))
    
    start_time = datetime.fromisoformat(session.get('quiz_start_time'))
    end_time = datetime.utcnow()
    time_taken = int((end_time - start_time).total_seconds())
    
    correct_count = 0
    wrong_count = 0
    total_score = 0
    
    for question_id in questions:
        q = Question.query.get(question_id)
        if not q:
            continue
        
        user_answer = request.form.get(f'q{question_id}')
        is_correct = user_answer == q.correct_answer
        
        if is_correct:
            correct_count += 1
            total_score += q.points
        else:
            wrong_count += 1
    
    game_result = GameResult(
        user_id=user_id,
        session_id=session.get('session_id'),
        category_id=category_id,
        total_questions=len(questions),
        correct_answers=correct_count,
        wrong_answers=wrong_count,
        score=total_score,
        time_taken_seconds=time_taken,
        game_end_time=end_time
    )
    db.session.add(game_result)
    db.session.flush()
    
    for question_id in questions:
        q = Question.query.get(question_id)
        user_answer = request.form.get(f'q{question_id}')
        
        answer = UserAnswer(
            result_id=game_result.result_id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=(user_answer == q.correct_answer),
            answered_at=datetime.utcnow()
        )
        db.session.add(answer)
    
    user = User.query.get(user_id)
    user.update_stats(total_score)
    
    analytics = UserAnalytics.query.filter_by(
        user_id=user_id, 
        category_id=category_id
    ).first()
    
    if not analytics:
        analytics = UserAnalytics(user_id=user_id, category_id=category_id)
        db.session.add(analytics)
    
    analytics.update_stats(correct_count, wrong_count, time_taken)
    
    db.session.commit()
    
    session.pop('quiz_questions', None)
    session.pop('quiz_category', None)
    session.pop('quiz_start_time', None)
    
    flash(f'Quiz completed! Score: {total_score}', 'success')
    return redirect(url_for('game.results_page', result_id=game_result.result_id))

# ========================================
# RESULTS ROUTE (RENAMED to avoid conflict)
# ========================================
@game_bp.route('/results/<int:result_id>')
def results_page(result_id):
    """Quiz results page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from models.game import GameResult, Category
    
    result = GameResult.query.get_or_404(result_id)
    
    if result.user_id != session['user_id']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('game.dashboard'))
    
    category = Category.query.get(result.category_id)
    
    minutes = result.time_taken_seconds // 60
    seconds = result.time_taken_seconds % 60
    time_str = f"{minutes}m {seconds:02d}s"
    
    display_score = min(result.score, 100)
    
    return render_template('results.html', 
                         category=category.category_name,
                         score=display_score,
                         total=100,
                         correct=result.correct_answers,
                         wrong=result.wrong_answers,
                         time_taken=time_str,
                         result_id=result_id)

# ========================================
# LEADERBOARD ROUTE
# ========================================
@game_bp.route('/leaderboard')
def leaderboard():
    """Leaderboard page"""
    from models.user import User
    from models.game import Category, GameResult
    
    top_users = User.query.filter_by(status='active')\
        .order_by(User.total_score.desc())\
        .limit(10).all()
    
    category_leaders = {}
    categories = Category.query.filter_by(status='active').all()
    
    for category in categories:
        top_result = GameResult.query.filter_by(category_id=category.category_id)\
            .order_by(GameResult.score.desc())\
            .first()
        
        if top_result:
            category_leaders[category.category_name] = {
                'score': top_result.score,
                'username': User.query.get(top_result.user_id).username
            }
    
    return render_template('leaderboard.html', 
                         top_users=top_users,
                         category_leaders=category_leaders)

# ========================================
# PROFILE ROUTE
# ========================================
@game_bp.route('/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from models.user import User
    from models.analytics import UserAnalytics
    from models.game import GameResult
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    analytics = UserAnalytics.query.filter_by(user_id=user_id).all()
    
    recent_games = GameResult.query.filter_by(user_id=user_id)\
        .order_by(GameResult.game_start_time.desc())\
        .limit(10).all()
    
    return render_template('profile.html', 
                         user=user, 
                         analytics=analytics,
                         recent_games=recent_games)