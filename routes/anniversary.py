# routes/anniversary.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Anniversary
from datetime import datetime, date

anniversary_bp = Blueprint('anniversary', __name__)

# 🎂 기념일 목록
@anniversary_bp.route('/anniversary')
@login_required
def index():
    anniversaries = Anniversary.query.filter_by(
        user_id=current_user.id
    ).order_by(Anniversary.date).all()
    
    # D-day 계산
    today = date.today()
    dday_list = []
    
    for ann in anniversaries:
        ann_date = ann.date
        
        # 매년 반복이면 올해 날짜로 변경
        if ann.repeat_yearly:
            ann_date = ann_date.replace(year=today.year)
            # 이미 지났으면 내년으로
            if ann_date < today:
                ann_date = ann_date.replace(year=today.year + 1)
        
        diff = (ann_date - today).days
        
        dday_list.append({
            'id': ann.id,
            'title': ann.title,
            'emoji': ann.emoji or '🎉',
            'date': ann_date.strftime('%Y-%m-%d'),
            'dday': diff,
            'dday_str': f'D-{diff}' if diff > 0 else ('D-Day!' if diff == 0 else f'D+{abs(diff)}')
        })
    
    # D-day 가까운 순으로 정렬
    dday_list.sort(key=lambda x: x['dday'])
    
    return render_template('anniversary.html',
        anniversaries=anniversaries,
        dday_list=dday_list
    )

# ➕ 기념일 추가
@anniversary_bp.route('/anniversary/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    date_str = request.form.get('date')
    emoji = request.form.get('emoji', '🎉')
    repeat_yearly = request.form.get('repeat_yearly') == 'on'
    
    if not title or not date_str:
        flash('기념일 이름과 날짜를 입력해주세요!', 'danger')
        return redirect(url_for('anniversary.index'))
    
    ann_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    new_ann = Anniversary(
        title=title,
        date=ann_date,
        emoji=emoji,
        repeat_yearly=repeat_yearly,
        user_id=current_user.id
    )
    
    db.session.add(new_ann)
    db.session.commit()
    
    flash('기념일이 추가됐어요! 🎂', 'success')
    return redirect(url_for('anniversary.index'))

# 🗑️ 기념일 삭제
@anniversary_bp.route('/anniversary/delete/<int:id>')
@login_required
def delete(id):
    ann = Anniversary.query.get_or_404(id)
    
    if ann.user_id != current_user.id:
        flash('권한이 없습니다!', 'danger')
        return redirect(url_for('anniversary.index'))
    
    db.session.delete(ann)
    db.session.commit()
    
    flash('기념일이 삭제됐어요!', 'info')
    return redirect(url_for('anniversary.index'))

# 📅 D-day API (메인 대시보드용)
@anniversary_bp.route('/api/anniversary/dday')
@login_required
def dday_api():
    anniversaries = Anniversary.query.filter_by(
        user_id=current_user.id
    ).all()
    
    today = date.today()
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
    return jsonify(dday_list[:5])  # 상위 5개만