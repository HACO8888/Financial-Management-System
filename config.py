import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """應用程式配置類別"""
    
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # 資料庫配置 - PostgreSQL
    # 從環境變數讀取 DATABASE_URL
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # 處理 psycopg3 驅動
    # SQLAlchemy 需要 postgresql+psycopg:// 來使用 psycopg3
    # 而不是默認的 postgresql:// (psycopg2)
    if DATABASE_URL:
        if DATABASE_URL.startswith('postgresql://'):
            # 檢查是否使用 psycopg3
            try:
                import psycopg
                # 將 postgresql:// 改為 postgresql+psycopg://
                DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)
            except ImportError:
                # 如果沒有 psycopg3，保持原樣使用 psycopg2
                pass
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # 設為 True 可以看到 SQL 查詢日誌
    
    # Session 配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # 生產環境設為 True (需要 HTTPS)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Flask-Login 配置
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    
    # 應用程式配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上傳 16MB
    
    # 預設類別配置
    DEFAULT_INCOME_CATEGORIES = [
        '薪資', '獎金', '獎助金', '投資收益', '兼職收入', '其他收入'
    ]
    
    DEFAULT_EXPENSE_CATEGORIES = [
        '飲食', '交通', '居住', '服飾', '娛樂', '教育',
        '醫療', '保險', '通訊', '日用品', '其他支出'
    ]
    
    # 排程任務配置
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Taipei'


class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """生產環境配置"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_ECHO = False  # 生產環境關閉 SQL 日誌
    
    # 生產環境應該從環境變數讀取
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("生產環境必須設定 SECRET_KEY 環境變數")


class TestingConfig(Config):
    """測試環境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 使用記憶體資料庫測試


# 根據環境變數選擇配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}