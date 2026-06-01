# routes/auth.py
from flask import Blueprint, jsonify,render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

# 📝 회원가입
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 이미 로그인한 상태면 메인으로
    if current_user.is_authenticated:
        return redirect(url_for('todos.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 이미 존재하는 유저인지 확인
        if User.query.filter_by(email=email).first():
            flash('이미 사용중인 이메일입니다!', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('이미 사용중인 아이디입니다!', 'danger')
            return redirect(url_for('auth.register'))
        
        # 비밀번호 암호화 후 저장
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('회원가입 완료! 로그인해주세요 😊', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


# 🔑 로그인
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todos.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        # 유저 없거나 비밀번호 틀리면
        if not user or not check_password_hash(user.password, password):
            flash('이메일 또는 비밀번호가 틀렸습니다!', 'danger')
            return redirect(url_for('auth.login'))
                
        login_user(user)
        flash(f'{user.username}님 환영합니다! 👋', 'success')
        return redirect(url_for('dashboard.index'))
            
    
    return render_template('login.html')


# 🚪 로그아웃
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃 되었습니다!', 'info')
    return redirect(url_for('auth.login'))



# 🔑 로그인 API
@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': '이메일 또는 비밀번호가 틀렸습니다!'}), 401

    login_user(user)
    return jsonify({'success': True, 'username': user.username})


# 📝 회원가입 API
@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': '이미 사용중인 이메일입니다!'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': '이미 사용중인 아이디입니다!'}), 400

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': True, 'message': '회원가입 완료! 로그인해주세요 😊'})