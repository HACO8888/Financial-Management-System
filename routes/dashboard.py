from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Transaction, Goal
from services.analysis_service import AnalysisService
from services.transaction_service import TransactionService
from datetime import datetime, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    """儀表板首頁"""
    # 獲取當前月份的統計資料
    today = datetime.now().date()
    first_day_of_month = today.replace(day=1)
    
    # 本月收入和支出
    monthly_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'income',
        Transaction.date >= first_day_of_month
    ).scalar() or 0
    
    monthly_expense = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense',
        Transaction.date >= first_day_of_month
    ).scalar() or 0
    
    # 本月淨收入
    net_income = float(monthly_income) - float(monthly_expense)
    
    # 最近 7 天的交易
    seven_days_ago = today - timedelta(days=7)
    recent_transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= seven_days_ago
    ).order_by(Transaction.date.desc(), Transaction.created_at.desc()).limit(10).all()
    
    # 進行中的目標
    active_goals = Goal.query.filter(
        Goal.user_id == current_user.id,
        Goal.status == 'active'
    ).all()
    
    # 計算每個目標的進度
    for goal in active_goals:
        goal.progress = goal.calculate_progress()
    
    # 獲取分析和建議
    analysis_service = AnalysisService(current_user.id)
    insights = analysis_service.get_monthly_insights()
    suggestions = analysis_service.get_suggestions()
    
    # 獲取本月類別統計（用於圖表）
    transaction_service = TransactionService(current_user.id)
    category_stats = transaction_service.get_monthly_category_stats(
        today.year, today.month
    )
    
    return render_template(
        'dashboard/index.html',
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        net_income=net_income,
        recent_transactions=recent_transactions,
        active_goals=active_goals,
        insights=insights,
        suggestions=suggestions,
        category_stats=category_stats
    )


@dashboard_bp.route('/quick-stats')
@login_required
def quick_stats():
    """快速統計資料（AJAX 端點）"""
    from flask import jsonify
    
    today = datetime.now().date()
    
    # 今日統計
    today_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'income',
        Transaction.date == today
    ).scalar() or 0
    
    today_expense = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense',
        Transaction.date == today
    ).scalar() or 0
    
    # 本週統計
    week_start = today - timedelta(days=today.weekday())
    week_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'income',
        Transaction.date >= week_start
    ).scalar() or 0
    
    week_expense = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense',
        Transaction.date >= week_start
    ).scalar() or 0
    
    return jsonify({
        'today': {
            'income': float(today_income),
            'expense': float(today_expense),
            'net': float(today_income) - float(today_expense)
        },
        'week': {
            'income': float(week_income),
            'expense': float(week_expense),
            'net': float(week_income) - float(week_expense)
        }
    })


# 導入 db 以供查詢使用
from models import db