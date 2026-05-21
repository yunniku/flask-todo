# routes/dashboard.py
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models import db, Todo, Goal, Anniversary, Diary
from datetime import datetime, date
import json
import calendar


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    today = date.today()
    
    # 📊 통계
    total_todos = Todo.query.filter_by(user_id=current_user.id).count()
    done_todos = Todo.query.filter_by(user_id=current_user.id, done=True).count()
    ongoing_todos = total_todos - done_todos
    
    # 오늘 할 일
    today_todos = Todo.query.filter_by(
        user_id=current_user.id
    ).filter(
        db.func.date(Todo.created_at) == today
    ).all()
    
    # 🎯 목표 달성률
    def calc_rate(goal_type):
        goals = Goal.query.filter_by(
            user_id=current_user.id,
            goal_type=goal_type
        ).all()
        if not goals:
            return 0
        achieved = sum(1 for g in goals if g.achieved)
        return round(achieved / len(goals) * 100)
    
    daily_rate = calc_rate('daily')
    weekly_rate = calc_rate('weekly')
    monthly_rate = calc_rate('monthly')
    
    # 🎂 D-day
    anniversaries = Anniversary.query.filter_by(
        user_id=current_user.id
    ).all()
    
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
    
    # 📔 오늘 다이어리
    today_diary = Diary.query.filter_by(
        user_id=current_user.id,
        date=today
    ).first()
    
    today_stickers = []
    if today_diary and today_diary.stickers:
        today_stickers = json.loads(today_diary.stickers)
    
    # 📅 캘린더용 이번 달 데이터
    year = today.year
    month = today.month
    
    # 이번 달 할 일 있는 날짜
    todo_dates = db.session.query(
        db.func.date(Todo.due_date)
    ).filter_by(user_id=current_user.id).filter(
        db.extract('year', Todo.due_date) == year,
        db.extract('month', Todo.due_date) == month
    ).distinct().all()
    todo_dates = [str(d[0]) for d in todo_dates if d[0]]
    
    # 이번 달 기념일 날짜
    ann_dates = []
    for ann in anniversaries:
        ann_date = ann.date
        if ann.repeat_yearly:
            ann_date = ann_date.replace(year=year)
        if ann_date.month == month:
            ann_dates.append(ann_date.strftime('%Y-%m-%d'))
    

    first_weekday = calendar.weekday(year, month, 1)
    first_weekday = (first_weekday + 1) % 7
    days_in_month = calendar.monthrange(year, month)[1]
    
    return render_template('dashboard.html',
        total_todos=total_todos,
        done_todos=done_todos,
        ongoing_todos=ongoing_todos,
        today_todos=today_todos,
        daily_rate=daily_rate,
        weekly_rate=weekly_rate,
        monthly_rate=monthly_rate,
        dday_list=dday_list[:5],
        today_diary=today_diary,
        today_stickers=today_stickers,
        year=year,
        month=month,
        todo_dates=todo_dates,
        ann_dates=ann_dates,
        today_str=today.strftime('%Y-%m-%d'),
        now_date=today.isoformat(),
        first_weekday=first_weekday,
        days_in_month=days_in_month
    )

# 📊 통계 페이지
@dashboard_bp.route('/stats')
@login_required
def stats():
    today = date.today()
    
    # 월별 완료 통계 (최근 6개월)
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
    
    # 카테고리별 통계
    categories = db.session.query(
        Todo.category,
        db.func.count(Todo.id).label('total'),
        db.func.sum(db.case((Todo.done == True, 1), else_=0)).label('done')
    ).filter_by(user_id=current_user.id).group_by(Todo.category).all()
    
    cat_stats = [{
        'category': c.category or '미분류',
        'total': c.total,
        'done': c.done or 0,
        'rate': round((c.done or 0) / c.total * 100) if c.total > 0 else 0
    } for c in categories]
    
    return render_template('stats.html',
        monthly_stats=monthly_stats,
        cat_stats=cat_stats,
        total_todos=Todo.query.filter_by(user_id=current_user.id).count(),
        done_todos=Todo.query.filter_by(user_id=current_user.id, done=True).count()
    )