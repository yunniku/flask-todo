# routes/calendar.py
import os
import json
from flask import Blueprint, redirect, url_for, session, request, flash, jsonify
from flask_login import login_required, current_user
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from models import db, Todo
from datetime import datetime, timezone

calendar_bp = Blueprint('calendar', __name__)

# 구글 캘린더 권한 범위
SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_SECRETS_FILE = 'credentials.json'

# 개발환경에서 HTTP 허용
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def get_calendar_service():
    """구글 캘린더 서비스 객체 반환"""
    if 'google_credentials' not in session:
        return None
    
    creds = Credentials(**session['google_credentials'])
    service = build('calendar', 'v3', credentials=creds)
    return service


def credentials_to_dict(credentials):
    """credentials 객체를 딕셔너리로 변환"""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


# 🔑 구글 로그인 시작
@calendar_bp.route('/google/login')
@login_required
def google_login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('calendar.oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)


# 🔄 구글 로그인 콜백
@calendar_bp.route('/oauth2callback')
@login_required
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('calendar.oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['google_credentials'] = credentials_to_dict(credentials)
    
    flash('구글 캘린더 연동 완료! 🎉', 'success')
    return redirect(url_for('todos.index'))


# 📅 할 일을 구글 캘린더에 추가
@calendar_bp.route('/calendar/add/<int:todo_id>')
@login_required
def add_to_calendar(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    
    if todo.user_id != current_user.id:
        flash('권한이 없습니다!', 'danger')
        return redirect(url_for('todos.index'))
    
    # 구글 연동 안 됐으면 로그인 먼저
    if 'google_credentials' not in session:
        flash('먼저 구글 캘린더를 연동해주세요!', 'warning')
        return redirect(url_for('calendar.google_login'))
    
    service = get_calendar_service()
    
    # 마감일 설정 (없으면 오늘)
    if todo.due_date:
        start_date = todo.due_date.isoformat()
        end_date = todo.due_date.isoformat()
    else:
        today = datetime.now().date()
        start_date = today.isoformat()
        end_date = today.isoformat()
    
    # 구글 캘린더 이벤트 만들기
    event = {
        'summary': f'[Todo] {todo.title}',
        'description': todo.content or '',
        'start': {
            'date': start_date,
            'timeZone': 'Asia/Seoul',
        },
        'end': {
            'date': end_date,
            'timeZone': 'Asia/Seoul',
        },
        'reminders': {
            'useDefault': True,
        },
    }
    
    try:
        event = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()
        flash(f'구글 캘린더에 추가됐어요! 📅', 'success')
    except Exception as e:
        flash('캘린더 추가 실패. 다시 연동해주세요!', 'danger')
        session.pop('google_credentials', None)
    
    return redirect(url_for('todos.index'))


# 🔌 구글 연동 해제
@calendar_bp.route('/google/logout')
@login_required
def google_logout():
    session.pop('google_credentials', None)
    flash('구글 캘린더 연동이 해제됐어요!', 'info')
    return redirect(url_for('todos.index'))


# 연동 상태 확인
@calendar_bp.route('/calendar/status')
@login_required
def calendar_status():
    connected = 'google_credentials' in session
    return jsonify({'connected': connected})