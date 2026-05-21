# config.py
import os

class Config:
    SECRET_KEY = 'my-super-secret-key-change-this-later'
    
    # MySQL 연결 설정
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:4050@localhost/flask_todo'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False  # 개발환경
    SESSION_COOKIE_HTTPONLY = True