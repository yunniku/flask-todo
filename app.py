# app.py
from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User

def create_app():
    app = Flask(__name__)
    
    # config.py 설정 불러오기
    app.config.from_object(Config)
    
    # DB 초기화
    db.init_app(app)
    
    # 로그인 매니저 초기화
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # 로그인 안 했을 때 이동할 페이지
    login_manager.login_message = '로그인이 필요합니다!'
    
    # 유저 세션 관리 (로그인 상태 유지)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 라우트(블루프린트) 등록
    from routes.auth import auth_bp
    from routes.todos import todos_bp
    from routes.api import api_bp
    from routes.calendar import calendar_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(todos_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(calendar_bp)

    # DB 테이블 생성
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)