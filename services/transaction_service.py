from models import db, Transaction, Category, Goal
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from decimal import Decimal


class TransactionService:
    """交易處理服務"""
    
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_transactions_by_date_range(self, start_date, end_date, transaction_type=None):
        """獲取指定日期範圍的交易記錄"""
        query = Transaction.query.filter(
            Transaction.user_id == self.user_id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
        
        if transaction_type:
            query = query.filter(Transaction.type == transaction_type)
        
        return query.order_by(Transaction.date.desc()).all()
    
    def get_monthly_summary(self, year, month):
        """獲取月度摘要統計"""
        # 計算月份的第一天和最後一天
        from calendar import monthrange
        last_day = monthrange(year, month)[1]
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, last_day).date()
        
        # 計算收入總額
        total_income = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'income',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).scalar() or Decimal('0')
        
        # 計算支出總額
        total_expense = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).scalar() or Decimal('0')
        
        # 計算淨額
        net_amount = total_income - total_expense
        
        # 計算交易筆數
        income_count = Transaction.query.filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'income',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).count()
        
        expense_count = Transaction.query.filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).count()
        
        return {
            'year': year,
            'month': month,
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'net_amount': float(net_amount),
            'income_count': income_count,
            'expense_count': expense_count,
            'total_count': income_count + expense_count
        }
    
    def get_monthly_category_stats(self, year, month):
        """獲取月度類別統計"""
        from calendar import monthrange
        last_day = monthrange(year, month)[1]
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, last_day).date()
        
        # 收入類別統計
        income_stats = db.session.query(
            Category.name,
            func.sum(Transaction.amount).label('total')
        ).join(Transaction).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'income',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).group_by(Category.name).all()
        
        # 支出類別統計
        expense_stats = db.session.query(
            Category.name,
            func.sum(Transaction.amount).label('total')
        ).join(Transaction).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).group_by(Category.name).all()
        
        return {
            'income': [{'category': name, 'amount': float(total)} for name, total in income_stats],
            'expense': [{'category': name, 'amount': float(total)} for name, total in expense_stats]
        }
    
    def get_daily_stats(self, year, month):
        """獲取每日統計（用於趨勢圖）"""
        from calendar import monthrange
        last_day = monthrange(year, month)[1]
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, last_day).date()
        
        # 按日期分組的收入
        daily_income = db.session.query(
            Transaction.date,
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'income',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).group_by(Transaction.date).all()
        
        # 按日期分組的支出
        daily_expense = db.session.query(
            Transaction.date,
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).group_by(Transaction.date).all()
        
        # 建立完整的日期範圍字典
        income_dict = {date: float(total) for date, total in daily_income}
        expense_dict = {date: float(total) for date, total in daily_expense}
        
        daily_data = []
        current_date = start_date
        while current_date <= end_date:
            daily_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'income': income_dict.get(current_date, 0),
                'expense': expense_dict.get(current_date, 0)
            })
            current_date += timedelta(days=1)
        
        return daily_data
    
    def get_top_expenses(self, year, month, limit=5):
        """獲取月度最大支出項目"""
        from calendar import monthrange
        last_day = monthrange(year, month)[1]
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, last_day).date()
        
        top_expenses = Transaction.query.filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).order_by(Transaction.amount.desc()).limit(limit).all()
        
        return [{
            'date': t.date.strftime('%Y-%m-%d'),
            'category': t.category.name,
            'amount': float(t.amount),
            'description': t.description or '無描述'
        } for t in top_expenses]
    
    def get_category_trend(self, category_id, months=6):
        """獲取特定類別的趨勢（最近 N 個月）"""
        today = datetime.now().date()
        start_date = today - timedelta(days=30 * months)
        
        monthly_data = db.session.query(
            extract('year', Transaction.date).label('year'),
            extract('month', Transaction.date).label('month'),
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == self.user_id,
            Transaction.category_id == category_id,
            Transaction.date >= start_date
        ).group_by('year', 'month').order_by('year', 'month').all()
        
        return [{
            'year': int(year),
            'month': int(month),
            'amount': float(total)
        } for year, month, total in monthly_data]
    
    def update_goals_progress(self):
        """更新所有進行中的目標進度"""
        from services.goal_service import GoalService
        
        goal_service = GoalService(self.user_id)
        
        # 獲取所有進行中的目標
        active_goals = Goal.query.filter_by(
            user_id=self.user_id,
            status='active'
        ).all()
        
        for goal in active_goals:
            goal_service.update_goal_progress(goal.id)
        
        db.session.commit()
    
    def calculate_average_daily_expense(self, days=30):
        """計算最近 N 天的平均每日支出"""
        today = datetime.now().date()
        start_date = today - timedelta(days=days)
        
        total_expense = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'expense',
            Transaction.date >= start_date,
            Transaction.date <= today
        ).scalar() or Decimal('0')
        
        return float(total_expense) / days
    
    def get_spending_by_weekday(self, year, month):
        """獲取按星期幾統計的支出（用於分析消費習慣）"""
        from calendar import monthrange
        last_day = monthrange(year, month)[1]
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, last_day).date()
        
        transactions = Transaction.query.filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).all()
        
        # 初始化星期統計
        weekday_stats = {i: {'total': 0, 'count': 0} for i in range(7)}
        weekday_names = ['週一', '週二', '週三', '週四', '週五', '週六', '週日']
        
        for t in transactions:
            weekday = t.date.weekday()
            weekday_stats[weekday]['total'] += float(t.amount)
            weekday_stats[weekday]['count'] += 1
        
        result = []
        for i in range(7):
            stats = weekday_stats[i]
            result.append({
                'weekday': weekday_names[i],
                'total': stats['total'],
                'count': stats['count'],
                'average': stats['total'] / stats['count'] if stats['count'] > 0 else 0
            })
        
        return result