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
    
    
# 현재 유저 정보
@api_bp.route('/me', methods=['GET'])
def me():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '로그인이 필요합니다!'}), 401
    return jsonify({
        'success': True,
        'user': {
            'id': current_user.id,
            'username': current_user.username
        }
    })

# 로그아웃
@api_bp.route('/logout', methods=['POST'])
@login_required
def api_logout():
    from flask_login import logout_user
    logout_user()
    return jsonify({'success': True})

# 📊 대시보드 API
@api_bp.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard():
    from datetime import date
    import json
    from models import Goal, Anniversary, Diary
    
    today = date.today()
    
    # 오늘 할 일
    today_todos = Todo.query.filter_by(user_id=current_user.id).filter(
        db.func.date(Todo.created_at) == today
    ).all()
    
    # 통계
    total = Todo.query.filter_by(user_id=current_user.id).count()
    done = Todo.query.filter_by(user_id=current_user.id, done=True).count()
    
    # 목표 달성률
    def calc_rate(goal_type):
        goals = Goal.query.filter_by(user_id=current_user.id, goal_type=goal_type).all()
        if not goals: return 0
        achieved = sum(1 for g in goals if g.achieved)
        return round(achieved / len(goals) * 100)
    
    # D-day
    anniversaries = Anniversary.query.filter_by(user_id=current_user.id).all()
    dday_list = []
    for ann in anniversaries:
        ann_date = ann.date
        if ann.repeat_yearly:
            ann_date = ann_date.replace(year=today.year)
            if ann_date < today:
                ann_date = ann_date.replace(year=today.year + 1)
        diff = (ann_date - today).days
        dday_list.append({
            'title': ann.title,
            'emoji': ann.emoji or '🎉',
            'dday': diff,
            'dday_str': f'D-{diff}' if diff > 0 else ('D-Day!' if diff == 0 else f'D+{abs(diff)}')
        })
    dday_list.sort(key=lambda x: x['dday'])

    # 오늘 다이어리
    today_diary = Diary.query.filter_by(user_id=current_user.id, date=today).first()

    return jsonify({
        'success': True,
        'today_todos': [
            {'id': t.id, 'title': t.title, 'done': t.done}
            for t in today_todos
        ],
        'ongoing_todos': total - done,
        'done_todos': done,
        'daily_rate': calc_rate('daily'),
        'weekly_rate': calc_rate('weekly'),
        'monthly_rate': calc_rate('monthly'),
        'dday_list': dday_list[:5],
        'today_diary': {
            'content': today_diary.content,
            'mood': today_diary.mood
        } if today_diary else None
    })
    
# 구글 캘린더 연동 상태
@api_bp.route('/google/status', methods=['GET'])
@login_required
def google_status():
    from routes.calendar import is_google_connected
    connected = is_google_connected()
    return jsonify({'connected': connected})    


# 🎂 기념일 목록
@api_bp.route('/anniversary', methods=['GET'])
@login_required
def get_anniversaries():
    from models import Anniversary
    today = datetime.now().date()
    anniversaries = Anniversary.query.filter_by(user_id=current_user.id).order_by(Anniversary.date).all()

    dday_list = []
    for ann in anniversaries:
        ann_date = ann.date
        if ann.repeat_yearly:
            ann_date = ann_date.replace(year=today.year)
            if ann_date < today:
                ann_date = ann_date.replace(year=today.year + 1)
        diff = (ann_date - today).days
        dday_list.append({
            'id': ann.id,
            'title': ann.title,
            'emoji': ann.emoji or '🎉',
            'date': ann_date.strftime('%Y-%m-%d'),
            'repeat_yearly': ann.repeat_yearly,
            'dday': diff,
            'dday_str': f'D-{diff}' if diff > 0 else ('D-Day!' if diff == 0 else f'D+{abs(diff)}')
        })

    dday_list.sort(key=lambda x: x['dday'])
    return jsonify({'success': True, 'anniversaries': dday_list})

# ➕ 기념일 추가
@api_bp.route('/anniversary', methods=['POST'])
@login_required
def create_anniversary():
    from models import Anniversary
    data = request.get_json()

    if not data.get('title') or not data.get('date'):
        return jsonify({'success': False, 'message': '기념일 이름과 날짜를 입력해주세요!'}), 400

    ann_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    new_ann = Anniversary(
        title=data['title'],
        date=ann_date,
        emoji=data.get('emoji', '🎉'),
        repeat_yearly=data.get('repeat_yearly', False),
        user_id=current_user.id
    )
    db.session.add(new_ann)
    db.session.commit()
    return jsonify({'success': True, 'message': '기념일이 추가됐어요! 🎂'})

# 🗑️ 기념일 삭제
@api_bp.route('/anniversary/<int:id>', methods=['DELETE'])
@login_required
def delete_anniversary(id):
    from models import Anniversary
    ann = Anniversary.query.get_or_404(id)
    if ann.user_id != current_user.id:
        return jsonify({'success': False, 'message': '권한이 없습니다!'}), 403
    db.session.delete(ann)
    db.session.commit()
    return jsonify({'success': True, 'message': '기념일이 삭제됐어요!'})


# 📊 통계 API
@api_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    from datetime import date
    today = datetime.now().date()

    monthly_stats = []
    for i in range(5, -1, -1):
        m = today.month - i
        y = today.year
        if m <= 0:
            m += 12
            y -= 1

        total = Todo.query.filter_by(user_id=current_user.id).filter(
            db.extract('year', Todo.created_at) == y,
            db.extract('month', Todo.created_at) == m
        ).count()

        done = Todo.query.filter_by(user_id=current_user.id, done=True).filter(
            db.extract('year', Todo.created_at) == y,
            db.extract('month', Todo.created_at) == m
        ).count()

        monthly_stats.append({
            'month': f'{y}/{m}',
            'total': total,
            'done': done,
            'rate': round(done / total * 100) if total > 0 else 0
        })

    from models import db as _db
    categories = _db.session.query(
        Todo.category,
        _db.func.count(Todo.id).label('total'),
        _db.func.sum(_db.case((Todo.done == True, 1), else_=0)).label('done')
    ).filter_by(user_id=current_user.id).group_by(Todo.category).all()

    cat_stats = [{
        'category': c.category or '미분류',
        'total': c.total,
        'done': c.done or 0,
        'rate': round((c.done or 0) / c.total * 100) if c.total > 0 else 0
    } for c in categories]

    total_todos = Todo.query.filter_by(user_id=current_user.id).count()
    done_todos = Todo.query.filter_by(user_id=current_user.id, done=True).count()

    return jsonify({
        'success': True,
        'monthly_stats': monthly_stats,
        'cat_stats': cat_stats,
        'total_todos': total_todos,
        'done_todos': done_todos
    })