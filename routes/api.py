# routes/api.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, Todo
from datetime import datetime

api_bp = Blueprint('api', __name__)

# 📋 전체 할 일 목록 가져오기
@api_bp.route('/todos', methods=['GET'])
@login_required
def get_todos():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        'success': True,
        'todos': [
            {
                'id': todo.id,
                'title': todo.title,
                'content': todo.content,
                'done': todo.done,
                'category': todo.category,
                'due_date': todo.due_date.strftime('%Y-%m-%d') if todo.due_date else None,
                'created_at': todo.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for todo in todos
        ]
    })


# 🔍 특정 할 일 하나 가져오기
@api_bp.route('/todos/<int:id>', methods=['GET'])
@login_required
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    
    if todo.user_id != current_user.id:
        return jsonify({'success': False, 'message': '권한이 없습니다!'}), 403
    
    return jsonify({
        'success': True,
        'todo': {
            'id': todo.id,
            'title': todo.title,
            'content': todo.content,
            'done': todo.done,
            'category': todo.category,
            'due_date': todo.due_date.strftime('%Y-%m-%d') if todo.due_date else None,
            'created_at': todo.created_at.strftime('%Y-%m-%d %H:%M')
        }
    })


# ➕ 새 할 일 추가
@api_bp.route('/todos', methods=['POST'])
@login_required
def create_todo():
    data = request.get_json()  # JSON 데이터 받기
    
    if not data or not data.get('title'):
        return jsonify({'success': False, 'message': '제목을 입력해주세요!'}), 400
    
    due_date = None
    if data.get('due_date'):
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
    
    new_todo = Todo(
        title=data['title'],
        content=data.get('content'),
        category=data.get('category'),
        due_date=due_date,
        user_id=current_user.id
    )
    
    db.session.add(new_todo)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '할 일이 추가됐어요! ✅',
        'todo': {
            'id': new_todo.id,
            'title': new_todo.title,
            'done': new_todo.done
        }
    }), 201


# ✏️ 할 일 수정
@api_bp.route('/todos/<int:id>', methods=['PUT'])
@login_required
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    
    if todo.user_id != current_user.id:
        return jsonify({'success': False, 'message': '권한이 없습니다!'}), 403
    
    data = request.get_json()
    
    if data.get('title'):
        todo.title = data['title']
    if data.get('content') is not None:
        todo.content = data['content']
    if data.get('category') is not None:
        todo.category = data['category']
    if data.get('due_date'):
        todo.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
    if data.get('done') is not None:
        todo.done = data['done']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '수정 완료! ✏️'
    })


# 🗑️ 할 일 삭제
@api_bp.route('/todos/<int:id>', methods=['DELETE'])
@login_required
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    
    if todo.user_id != current_user.id:
        return jsonify({'success': False, 'message': '권한이 없습니다!'}), 403
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '삭제됐어요! 🗑️'
    })