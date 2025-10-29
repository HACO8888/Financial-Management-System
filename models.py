from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """使用者模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # 關聯
    categories = db.relationship('Category', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    monthly_reports = db.relationship('MonthlyReport', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """設定密碼（加密）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """檢查密碼"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """類別模型（收入/支出分類）"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' 或 'expense'
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # 關聯
    transactions = db.relationship('Transaction', backref='category', lazy='dynamic')
    
    __table_args__ = (
        CheckConstraint("type IN ('income', 'expense')", name='check_category_type'),
        db.UniqueConstraint('user_id', 'name', 'type', name='unique_user_category'),
    )
    
    def __repr__(self):
        return f'<Category {self.name} ({self.type})>'


class Transaction(db.Model):
    """交易記錄模型"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' 或 'expense'
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        CheckConstraint("type IN ('income', 'expense')", name='check_transaction_type'),
        CheckConstraint("amount > 0", name='check_positive_amount'),
    )
    
    def __repr__(self):
        return f'<Transaction {self.type} ${self.amount} on {self.date}>'


class Goal(db.Model):
    """財務目標模型"""
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Numeric(12, 2), nullable=False)
    current_amount = db.Column(db.Numeric(12, 2), default=0)
    goal_type = db.Column(db.String(20), nullable=False)  # 'saving', 'expense_limit'
    period = db.Column(db.String(20), nullable=False)  # 'monthly', 'yearly', 'custom'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        CheckConstraint("goal_type IN ('saving', 'expense_limit')", name='check_goal_type'),
        CheckConstraint("period IN ('monthly', 'yearly', 'custom')", name='check_period'),
        CheckConstraint("status IN ('active', 'completed', 'cancelled')", name='check_status'),
        CheckConstraint("target_amount > 0", name='check_positive_target'),
    )
    
    def calculate_progress(self):
        """計算目標進度百分比"""
        if self.target_amount == 0:
            return 0
        progress = (float(self.current_amount) / float(self.target_amount)) * 100
        return min(progress, 100)  # 最多 100%
    
    def __repr__(self):
        return f'<Goal {self.name} ({self.status})>'


class MonthlyReport(db.Model):
    """月報表模型"""
    __tablename__ = 'monthly_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    total_income = db.Column(db.Numeric(12, 2), default=0)
    total_expense = db.Column(db.Numeric(12, 2), default=0)
    net_amount = db.Column(db.Numeric(12, 2), default=0)
    report_data = db.Column(db.JSON)  # 儲存詳細分析資料
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'year', 'month', name='unique_user_month'),
        CheckConstraint("month >= 1 AND month <= 12", name='check_valid_month'),
    )
    
    def __repr__(self):
        return f'<MonthlyReport {self.year}-{self.month:02d} User {self.user_id}>'