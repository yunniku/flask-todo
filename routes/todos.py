
#C (Create) → 할 일 추가 /add
#R (Read)   → 할 일 목록 /
#U (Update) → 할 일 수정 /edit/<id>
#D (Delete) → 할 일 삭제 /delete/<id>

# routes/todos.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Todo
from datetime import datetime
from flask import session


todos_bp = Blueprint('todos', __name__)

# 📋 메인 페이지 - 할 일 목록
@todos_bp.route('/')
@login_required
def index():
    category = request.args.get('category')  # 카테고리 필터
    
    if category:
        todos = Todo.query.filter_by(
            user_id=current_user.id,
            category=category
        ).order_by(Todo.created_at.desc()).all()
    else:
        todos = Todo.query.filter_by(
            user_id=current_user.id
        ).order_by(Todo.created_at.desc()).all()
    
    # 카테고리 목록 (드롭다운용)
    categories = db.session.query(Todo.category).filter_by(
        user_id=current_user.id
    ).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    google_connected = 'google_credentials' in session

    return render_template('todos.html', 
        todos=todos, 
        categories=categories, 
        selected_category=category,
        google_connected=google_connected
    )
# ➕ 할 일 추가
@todos_bp.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    content = request.form.get('content')
    category = request.form.get('category')
    due_date_str = request.form.get('due_date')
    
    if not title:
        flash('할 일 제목을 입력해주세요!', 'danger')
        return redirect(url_for('todos.index'))
    
    # 마감일 변환 (문자열 → 날짜)
    due_date = None
    if due_date_str:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    
    new_todo = Todo(
        title=title,
        content=content,
        category=category,
        due_date=due_date,
        user_id=current_user.id
    )
    
    db.session.add(new_todo)
    db.session.commit()
    
    flash('할 일이 추가됐어요! ✅', 'success')
    return redirect(url_for('todos.index'))


# ✏️ 할 일 수정
@todos_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    todo = Todo.query.get_or_404(id)
    
    # 다른 유저의 할 일 수정 차단
    if todo.user_id != current_user.id:
        flash('권한이 없습니다!', 'danger')
        return redirect(url_for('todos.index'))
    
    if request.method == 'POST':
        todo.title = request.form.get('title')
        todo.content = request.form.get('content')
        todo.category = request.form.get('category')
        due_date_str = request.form.get('due_date')
        
        if due_date_str:
            todo.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        
        db.session.commit()
        flash('수정 완료! ✏️', 'success')
        return redirect(url_for('todos.index'))
    
    return render_template('edit.html', todo=todo)


# ✅ 완료/미완료 토글
@todos_bp.route('/toggle/<int:id>')
@login_required
def toggle(id):
    todo = Todo.query.get_or_404(id)
    
    if todo.user_id != current_user.id:
        flash('권한이 없습니다!', 'danger')
        return redirect(url_for('todos.index'))
    
    # True → False, False → True
    todo.done = not todo.done
    db.session.commit()
    
    return redirect(url_for('todos.index'))


# 🗑️ 할 일 삭제
@todos_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    
    if todo.user_id != current_user.id:
        flash('권한이 없습니다!', 'danger')
        return redirect(url_for('todos.index'))
    
    db.session.delete(todo)
    db.session.commit()
    
    flash('삭제됐어요! 🗑️', 'info')
    return redirect(url_for('todos.index'))