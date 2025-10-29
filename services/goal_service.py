from models import db, Goal, Transaction
from sqlalchemy import func
from datetime import datetime, date
from decimal import Decimal


class GoalService:
    """財務目標服務"""
    
    def __init__(self, user_id):
        self.user_id = user_id
    
    def update_goal_progress(self, goal_id):
        """更新目標進度"""
        goal = Goal.query.filter_by(id=goal_id, user_id=self.user_id).first()
        
        if not goal or goal.status != 'active':
            return None
        
        # 根據目標類型計算進度
        if goal.goal_type == 'saving':
            # 儲蓄目標：計算期間內的淨收入
            current_amount = self._calculate_net_income(
                goal.start_date,
                goal.end_date or datetime.now().date()
            )
        
        elif goal.goal_type == 'expense_limit':
            # 支出限制目標：計算期間內的總支出
            current_amount = self._calculate_total_expense(
                goal.start_date,
                goal.end_date or datetime.now().date()
            )
        
        else:
            return None
        
        # 更新目標的當前金額
        goal.current_amount = current_amount
        
        # 檢查是否達成目標
        if goal.goal_type == 'saving':
            # 儲蓄目標：當前金額 >= 目標金額
            if current_amount >= goal.target_amount:
                goal.status = 'completed'
        
        elif goal.goal_type == 'expense_limit':
            # 支出限制目標：特殊處理，不自動標記為完成
            # 因為支出可能會繼續增加
            pass
        
        db.session.commit()
        return goal
    
    def _calculate_net_income(self, start_date, end_date):
        """計算淨收入（收入 - 支出）"""
        # 計算總收入
        total_income = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'income',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).scalar() or Decimal('0')
        
        # 計算總支出
        total_expense = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).scalar() or Decimal('0')
        
        return total_income - total_expense
    
    def _calculate_total_expense(self, start_date, end_date):
        """計算總支出"""
        total_expense = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).scalar() or Decimal('0')
        
        return total_expense
    
    def is_goal_overdue(self, goal):
        """檢查目標是否已過期"""
        if goal.status != 'active' or not goal.end_date:
            return False
        
        today = datetime.now().date()
        return today > goal.end_date
    
    def get_goal_statistics(self, goal_id):
        """獲取目標的詳細統計資料"""
        goal = Goal.query.filter_by(id=goal_id, user_id=self.user_id).first()
        
        if not goal:
            return None
        
        # 計算目標進度百分比
        progress_percent = goal.calculate_progress()
        
        # 計算剩餘金額
        remaining_amount = float(goal.target_amount - goal.current_amount)
        
        # 計算已過天數和剩餘天數
        today = datetime.now().date()
        days_passed = (today - goal.start_date).days
        
        if goal.end_date:
            total_days = (goal.end_date - goal.start_date).days
            days_remaining = (goal.end_date - today).days
        else:
            total_days = None
            days_remaining = None
        
        # 計算日均進度（如果適用）
        if days_passed > 0:
            daily_average = float(goal.current_amount) / days_passed
        else:
            daily_average = 0
        
        # 預估完成日期（基於當前進度）
        estimated_completion_date = None
        if daily_average > 0 and remaining_amount > 0:
            days_needed = int(remaining_amount / daily_average)
            estimated_completion_date = today + timedelta(days=days_needed)
        
        # 獲取相關交易記錄
        if goal.goal_type == 'saving':
            # 儲蓄目標：顯示收入和支出
            transactions = Transaction.query.filter(
                Transaction.user_id == self.user_id,
                Transaction.date >= goal.start_date,
                Transaction.date <= (goal.end_date or today)
            ).order_by(Transaction.date.desc()).limit(10).all()
        
        elif goal.goal_type == 'expense_limit':
            # 支出限制目標：只顯示支出
            transactions = Transaction.query.filter(
                Transaction.user_id == self.user_id,
                Transaction.type == 'expense',
                Transaction.date >= goal.start_date,
                Transaction.date <= (goal.end_date or today)
            ).order_by(Transaction.date.desc()).limit(10).all()
        
        else:
            transactions = []
        
        return {
            'progress_percent': progress_percent,
            'current_amount': float(goal.current_amount),
            'target_amount': float(goal.target_amount),
            'remaining_amount': remaining_amount,
            'days_passed': days_passed,
            'days_remaining': days_remaining,
            'total_days': total_days,
            'daily_average': daily_average,
            'estimated_completion_date': estimated_completion_date,
            'is_overdue': self.is_goal_overdue(goal),
            'recent_transactions': transactions
        }
    
    def get_goal_progress_history(self, goal_id):
        """獲取目標的歷史進度（按週統計）"""
        goal = Goal.query.filter_by(id=goal_id, user_id=self.user_id).first()
        
        if not goal:
            return []
        
        from datetime import timedelta
        
        history = []
        current_date = goal.start_date
        today = datetime.now().date()
        end_date = min(goal.end_date or today, today)
        
        while current_date <= end_date:
            # 計算到當前日期的進度
            if goal.goal_type == 'saving':
                amount = self._calculate_net_income(goal.start_date, current_date)
            else:
                amount = self._calculate_total_expense(goal.start_date, current_date)
            
            history.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'amount': float(amount),
                'progress': (float(amount) / float(goal.target_amount) * 100) if goal.target_amount > 0 else 0
            })
            
            # 每週記錄一次
            current_date += timedelta(days=7)
        
        return history
    
    def get_all_active_goals_summary(self):
        """獲取所有進行中目標的摘要"""
        active_goals = Goal.query.filter_by(
            user_id=self.user_id,
            status='active'
        ).all()
        
        summary = {
            'total_goals': len(active_goals),
            'on_track': 0,
            'behind': 0,
            'overdue': 0,
            'goals': []
        }
        
        for goal in active_goals:
            # 更新進度
            self.update_goal_progress(goal.id)
            
            progress = goal.calculate_progress()
            is_overdue = self.is_goal_overdue(goal)
            
            # 計算預期進度
            if goal.end_date:
                total_days = (goal.end_date - goal.start_date).days
                days_passed = (datetime.now().date() - goal.start_date).days
                expected_progress = (days_passed / total_days * 100) if total_days > 0 else 0
            else:
                expected_progress = 0
            
            # 分類目標狀態
            if is_overdue:
                summary['overdue'] += 1
                status = 'overdue'
            elif progress >= expected_progress:
                summary['on_track'] += 1
                status = 'on_track'
            else:
                summary['behind'] += 1
                status = 'behind'
            
            summary['goals'].append({
                'id': goal.id,
                'name': goal.name,
                'progress': progress,
                'status': status,
                'current_amount': float(goal.current_amount),
                'target_amount': float(goal.target_amount)
            })
        
        return summary
    
    def suggest_goal_adjustment(self, goal_id):
        """根據當前進度建議調整目標"""
        goal = Goal.query.filter_by(id=goal_id, user_id=self.user_id).first()
        
        if not goal or goal.status != 'active':
            return None
        
        stats = self.get_goal_statistics(goal_id)
        suggestions = []
        
        # 如果進度落後且有截止日期
        if goal.end_date and stats['days_remaining'] and stats['days_remaining'] > 0:
            progress = stats['progress_percent']
            expected_progress = (stats['days_passed'] / stats['total_days'] * 100) if stats['total_days'] > 0 else 0
            
            if progress < expected_progress * 0.8:  # 落後超過 20%
                # 計算需要的日均進度
                required_daily = stats['remaining_amount'] / stats['days_remaining']
                suggestions.append({
                    'type': 'increase_effort',
                    'message': f'目標進度落後，建議每日增加 ${required_daily:.2f} 以達成目標'
                })
            
            elif progress < expected_progress:
                suggestions.append({
                    'type': 'slight_behind',
                    'message': '目標進度略微落後，請保持努力'
                })
            
            else:
                suggestions.append({
                    'type': 'on_track',
                    'message': '目標進度良好，繼續保持！'
                })
        
        # 如果已過期但未完成
        if self.is_goal_overdue(goal) and goal.current_amount < goal.target_amount:
            suggestions.append({
                'type': 'overdue',
                'message': '目標已過期，建議調整目標金額或延長期限'
            })
        
        return suggestions


from datetime import timedelta