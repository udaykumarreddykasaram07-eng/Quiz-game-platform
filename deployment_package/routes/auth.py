from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.user_id
            session['username'] = user.username
            user.last_login = datetime.utcnow()
            
            from models.game import GameSession
            new_session = GameSession(
                user_id=user.user_id,
                ip_address=request.remote_addr,
                device_type=request.user_agent.platform or 'Unknown',
                browser_info=request.user_agent.browser or 'Unknown'
            )
            from extensions import db
            db.session.add(new_session)
            db.session.commit()
            
            session['session_id'] = new_session.session_id
            flash('Login successful!', 'success')
            return redirect(url_for('game.dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html', error='All fields are required')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html', error='Passwords do not match')
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists', 'error')
            return render_template('register.html', error='Username or email already exists')
        
        new_user = User(username=username, email=email, full_name=full_name)
        new_user.set_password(password)
        
        from extensions import db
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))