from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from config import config
from models import db, User
import os


def create_app(config_name='development'):
    """應用程式工廠函數"""
    app = Flask(__name__)
    
    # 載入配置
    app.config.from_object(config[config_name])
    
    # 初始化擴展
    db.init_app(app)
    
    # 初始化 Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '請先登入以訪問此頁面'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 註冊藍圖
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.transactions import transactions_bp
    from routes.goals import goals_bp
    from routes.reports import reports_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(reports_bp)
    
    # 首頁路由
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    # 錯誤處理
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # 初始化資料庫和排程任務
    with app.app_context():
        # 建立資料表
        db.create_all()
        
        # 初始化排程器（每月自動生成報表）
        from utils.scheduler import init_scheduler
        init_scheduler(app)
    
    return app


if __name__ == '__main__':
    # 從環境變數讀取配置，預設為 development
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    
    # 開發環境配置
    debug_mode = env == 'development'
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 財務管理系統啟動中...")
    print(f"📊 環境: {env}")
    print(f"🌐 訪問網址: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)