# app.py
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from config import Config
from models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    CORS(app, supports_credentials=True)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '로그인이 필요합니다!'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from routes.auth import auth_bp
    from routes.todos import todos_bp
    from routes.api import api_bp
    from routes.calendar import calendar_bp
    from routes.goals import goals_bp
    from routes.anniversary import anniversary_bp
    from routes.diary import diary_bp
    from routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(todos_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(calendar_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(anniversary_bp)
    app.register_blueprint(diary_bp)
    app.register_blueprint(dashboard_bp)
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)