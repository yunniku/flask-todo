# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# 👤 유저 테이블
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)       # 고유 번호
    username = db.Column(db.String(50), unique=True, nullable=False)   # 아이디
    email = db.Column(db.String(120), unique=True, nullable=False)     # 이메일
    password = db.Column(db.String(200), nullable=False)               # 비밀번호
    created_at = db.Column(db.DateTime, default=datetime.utcnow)       # 가입일

    # 유저와 할 일 연결 (1명이 여러 개의 할 일을 가짐)
    todos = db.relationship('Todo', backref='user', lazy=True)

# 📝 할 일 테이블
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)          # 고유 번호
    title = db.Column(db.String(200), nullable=False)     # 할 일 제목
    content = db.Column(db.Text, nullable=True)           # 상세 내용
    done = db.Column(db.Boolean, default=False)           # 완료 여부
    due_date = db.Column(db.Date, nullable=True)          # 마감일
    category = db.Column(db.String(50), nullable=True)   # 카테고리
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 생성일

    # 어떤 유저의 할 일인지 연결
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)