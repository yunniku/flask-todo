# routes/diary.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Diary
from datetime import datetime, date
import json

diary_bp = Blueprint('diary', __name__)

# 📔 다이어리 목록
@diary_bp.route('/diary')
@login_required
def index():
    year = request.args.get('year', date.today().year, type=int)
    month = request.args.get('month', date.today().month, type=int)
    
    # 해당 월 다이어리 목록
    diaries = Diary.query.filter_by(
        user_id=current_user.id
    ).filter(
        db.extract('year', Diary.date) == year,
        db.extract('month', Diary.date) == month
    ).order_by(Diary.date.desc()).all()
    
    # 오늘 다이어리
    today_diary = Diary.query.filter_by(
        user_id=current_user.id,
        date=date.today()
    ).first()
    
    return render_template('diary.html',
        diaries=diaries,
        today_diary=today_diary,
        year=year,
        month=month
    )

# 📝 다이어리 작성/수정
@diary_bp.route('/diary/save', methods=['POST'])
@login_required
def save():
    date_str = request.form.get('date', date.today().isoformat())
    content = request.form.get('content', '')
    mood = request.form.get('mood', '')
    stickers = request.form.getlist('stickers')
    theme_color = request.form.get('theme_color', 'purple')
    
    diary_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # 같은 날짜 다이어리 있으면 수정, 없으면 새로 만들기
    diary = Diary.query.filter_by(
        user_id=current_user.id,
        date=diary_date
    ).first()
    
    if diary:
        diary.content = content
        diary.mood = mood
        diary.stickers = json.dumps(stickers)
        diary.theme_color = theme_color
    else:
        diary = Diary(
            date=diary_date,
            content=content,
            mood=mood,
            stickers=json.dumps(stickers),
            theme_color=theme_color,
            user_id=current_user.id
        )
        db.session.add(diary)
    
    db.session.commit()
    flash('다이어리가 저장됐어요! 📔', 'success')
    return redirect(url_for('diary.index'))

# 📖 특정 날짜 다이어리 보기
@diary_bp.route('/diary/<string:date_str>')
@login_required
def view(date_str):
    diary_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    diary = Diary.query.filter_by(
        user_id=current_user.id,
        date=diary_date
    ).first()
    
    stickers = []
    if diary and diary.stickers:
        stickers = json.loads(diary.stickers)
    
    return render_template('diary_view.html',
        diary=diary,
        diary_date=diary_date,
        stickers=stickers
    )

# 🗑️ 다이어리 삭제
@diary_bp.route('/diary/delete/<int:id>')
@login_required
def delete(id):
    diary = Diary.query.get_or_404(id)
    
    if diary.user_id != current_user.id:
        flash('권한이 없습니다!', 'danger')
        return redirect(url_for('diary.index'))
    
    db.session.delete(diary)
    db.session.commit()
    
    flash('다이어리가 삭제됐어요!', 'info')
    return redirect(url_for('diary.index'))

# 📊 다이어리 API (캘린더용)
@diary_bp.route('/api/diary/dates')
@login_required
def dates_api():
    year = request.args.get('year', date.today().year, type=int)
    month = request.args.get('month', date.today().month, type=int)
    
    diaries = Diary.query.filter_by(
        user_id=current_user.id
    ).filter(
        db.extract('year', Diary.date) == year,
        db.extract('month', Diary.date) == month
    ).all()
    
    return jsonify([{
        'date': d.date.isoformat(),
        'mood': d.mood,
        'theme_color': d.theme_color
    } for d in diaries])
    
    