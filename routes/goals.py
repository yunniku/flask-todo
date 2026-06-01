# routes/goals.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Goal
from datetime import datetime, date

goals_bp = Blueprint('goals', __name__)

# 🎯 목표 목록
@goals_bp.route('/goals')
@login_required
def index():
    daily_goals = Goal.query.filter_by(
        user_id=current_user.id,
        goal_type='daily'
    ).order_by(Goal.created_at.desc()).all()
    
    weekly_goals = Goal.query.filter_by(
        user_id=current_user.id,
        goal_type='weekly'
    ).order_by(Goal.created_at.desc()).all()
    
    monthly_goals = Goal.query.filter_by(
        user_id=current_user.id,
        goal_type='monthly'
    ).order_by(Goal.created_at.desc()).all()
    
    # 달성률 계산
    def calc_rate(goals):
        if not goals:
            return 0
        achieved = sum(1 for g in goals if g.achieved)
        return round(achieved / len(goals) * 100)
    
    return render_template('goals.html',
        daily_goals=daily_goals,
        weekly_goals=weekly_goals,
        monthly_goals=monthly_goals,
        daily_rate=calc_rate(daily_goals),
        weekly_rate=calc_rate(weekly_goals),
        monthly_rate=calc_rate(monthly_goals)
    )

# ➕ 목표 추가
@goals_bp.route('/goals/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    goal_type = request.form.get('goal_type')
    target_date_str = request.form.get('target_date')
    
    if not title or not goal_type:
        flash('목표 제목과 종류를 입력해주세요!', 'danger')
        return redirect(url_for('goals.index'))
    
    target_date = None
    if target_date_str:
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
    
    new_goal = Goal(
        title=title,
        description=description,
        goal_type=goal_type,
        target_date=target_date,
        user_id=current_user.id
    )
    
    db.session.add(new_goal)
    db.session.commit()
    
    flash('목표가 추가됐어요! 🎯', 'success')
    return redirect(url_for('goals.index'))

# ✅ 목표 달성/미달성 토글
@goals_bp.route('/goals/toggle/<int:id>')
@login_required
def toggle(id):
    goal = Goal.query.get_or_404(id)
    
    if goal.user_id != current_user.id:
        flash('권한이 없습니다!', 'danger')
        return redirect(url_for('goals.index'))
    
    goal.achieved = not goal.achieved
    db.session.commit()
    
    return redirect(url_for('goals.index'))

# 🗑️ 목표 삭제
@goals_bp.route('/goals/delete/<int:id>')
@login_required
def delete(id):
    goal = Goal.query.get_or_404(id)
    
    if goal.user_id != current_user.id:
        flash('권한이 없습니다!', 'danger')
        return redirect(url_for('goals.index'))
    
    db.session.delete(goal)
    db.session.commit()
    
    flash('목표가 삭제됐어요!', 'info')
    return redirect(url_for('goals.index'))

# 📊 달성률 API
@goals_bp.route('/api/goals/rate')
@login_required
def rate():
    goal_type = request.args.get('type', 'daily')
    goals = Goal.query.filter_by(
        user_id=current_user.id,
        goal_type=goal_type
    ).all()
    
    if not goals:
        return jsonify({'rate': 0, 'total': 0, 'achieved': 0})
    
    achieved = sum(1 for g in goals if g.achieved)
    rate = round(achieved / len(goals) * 100)
    
    return jsonify({
        'rate': rate,
        'total': len(goals),
        'achieved': achieved
    })
    