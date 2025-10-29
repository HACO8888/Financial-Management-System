from models import db, Transaction, Category, Goal
from services.transaction_service import TransactionService
from services.goal_service import GoalService
from sqlalchemy import func
from datetime import datetime, timedelta
from decimal import Decimal


class AnalysisService:
    """分析和建議服務"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.transaction_service = TransactionService(user_id)
        self.goal_service = GoalService(user_id)
    
    def get_monthly_insights(self):
        """獲取本月的分析見解"""
        today = datetime.now().date()
        current_year = today.year
        current_month = today.month
        
        # 獲取本月摘要
        summary = self.transaction_service.get_monthly_summary(current_year, current_month)
        
        insights = []
        
        # 1. 收支狀況分析
        if summary['net_amount'] > 0:
            insights.append({
                'type': 'success',
                'icon': '✅',
                'title': '收支健康',
                'message': f'本月淨收入 ${summary["net_amount"]:.2f}，財務狀況良好'
            })
        elif summary['net_amount'] < 0:
            insights.append({
                'type': 'warning',
                'icon': '⚠️',
                'title': '收支警告',
                'message': f'本月支出超過收入 ${abs(summary["net_amount"]):.2f}，請注意控制支出'
            })
        
        # 2. 支出趨勢分析
        expense_trend = self._analyze_expense_trend()
        if expense_trend:
            insights.append(expense_trend)
        
        # 3. 異常支出檢測
        abnormal_expenses = self._detect_abnormal_expenses()
        if abnormal_expenses:
            insights.append(abnormal_expenses)
        
        # 4. 儲蓄率分析
        if summary['total_income'] > 0:
            savings_rate = (summary['net_amount'] / summary['total_income']) * 100
            
            if savings_rate < 10:
                insights.append({
                    'type': 'warning',
                    'icon': '💰',
                    'title': '儲蓄率偏低',
                    'message': f'本月儲蓄率僅 {savings_rate:.1f}%，建議提高至 20% 以上'
                })
            elif savings_rate >= 30:
                insights.append({
                    'type': 'success',
                    'icon': '🎉',
                    'title': '儲蓄表現優異',
                    'message': f'本月儲蓄率達 {savings_rate:.1f}%，繼續保持！'
                })
        
        # 5. 目標進度提醒
        goal_reminders = self._get_goal_reminders()
        insights.extend(goal_reminders)
        
        return insights
    
    def get_suggestions(self):
        """獲取理財建議"""
        suggestions = []
        
        # 1. 預算建議
        budget_suggestion = self._suggest_budget_optimization()
        if budget_suggestion:
            suggestions.append(budget_suggestion)
        
        # 2. 類別優化建議
        category_suggestions = self._suggest_category_optimization()
        suggestions.extend(category_suggestions)
        
        # 3. 儲蓄建議
        savings_suggestion = self._suggest_savings_improvement()
        if savings_suggestion:
            suggestions.append(savings_suggestion)
        
        # 4. 目標建議
        goal_suggestions = self._suggest_goal_adjustments()
        suggestions.extend(goal_suggestions)
        
        return suggestions
    
    def _analyze_expense_trend(self):
        """分析支出趨勢"""
        today = datetime.now().date()
        
        # 獲取最近三個月的支出
        expenses = []
        for i in range(3):
            month_offset = i
            if today.month - month_offset < 1:
                year = today.year - 1
                month = 12 + (today.month - month_offset)
            else:
                year = today.year
                month = today.month - month_offset
            
            summary = self.transaction_service.get_monthly_summary(year, month)
            expenses.append(summary['total_expense'])
        
        expenses.reverse()  # 從舊到新排序
        
        # 檢查趨勢
        if len(expenses) >= 2:
            recent_change = ((expenses[-1] - expenses[-2]) / expenses[-2] * 100) if expenses[-2] > 0 else 0
            
            if recent_change > 20:
                return {
                    'type': 'warning',
                    'icon': '📈',
                    'title': '支出上升趨勢',
                    'message': f'最近支出增加 {recent_change:.1f}%，建議檢視非必要開銷'
                }
            elif recent_change < -20:
                return {
                    'type': 'success',
                    'icon': '📉',
                    'title': '支出控制良好',
                    'message': f'支出較上月減少 {abs(recent_change):.1f}%，表現優異！'
                }
        
        return None
    
    def _detect_abnormal_expenses(self):
        """檢測異常支出"""
        today = datetime.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # 獲取最近 30 天的支出
        recent_expenses = Transaction.query.filter(
            Transaction.user_id == self.user_id,
            Transaction.type == 'expense',
            Transaction.date >= thirty_days_ago,
            Transaction.date <= today
        ).all()
        
        if not recent_expenses:
            return None
        
        # 計算平均值和標準差
        amounts = [float(t.amount) for t in recent_expenses]
        avg_amount = sum(amounts) / len(amounts)
        
        # 找出異常高額支出（超過平均值 2 倍）
        abnormal = [t for t in recent_expenses if float(t.amount) > avg_amount * 2]
        
        if abnormal:
            max_abnormal = max(abnormal, key=lambda t: t.amount)
            return {
                'type': 'info',
                'icon': '🔍',
                'title': '發現高額支出',
                'message': f'在「{max_abnormal.category.name}」類別有 ${float(max_abnormal.amount):.2f} 的大額支出'
            }
        
        return None
    
    def _get_goal_reminders(self):
        """獲取目標進度提醒"""
        reminders = []
        
        active_goals = Goal.query.filter_by(
            user_id=self.user_id,
            status='active'
        ).all()
        
        for goal in active_goals:
            # 更新進度
            self.goal_service.update_goal_progress(goal.id)
            
            progress = goal.calculate_progress()
            
            # 即將完成的目標
            if 80 <= progress < 100:
                reminders.append({
                    'type': 'info',
                    'icon': '🎯',
                    'title': f'目標「{goal.name}」即將達成',
                    'message': f'已完成 {progress:.1f}%，再加把勁！'
                })
            
            # 已完成的目標
            elif progress >= 100:
                reminders.append({
                    'type': 'success',
                    'icon': '🏆',
                    'title': f'恭喜！目標「{goal.name}」已達成',
                    'message': '點擊標記為完成'
                })
            
            # 進度落後的目標
            elif goal.end_date:
                today = datetime.now().date()
                total_days = (goal.end_date - goal.start_date).days
                days_passed = (today - goal.start_date).days
                expected_progress = (days_passed / total_days * 100) if total_days > 0 else 0
                
                if progress < expected_progress * 0.7:  # 落後超過 30%
                    reminders.append({
                        'type': 'warning',
                        'icon': '⏰',
                        'title': f'目標「{goal.name}」進度落後',
                        'message': f'當前進度 {progress:.1f}%，需要加快努力'
                    })
        
        return reminders
    
    def _suggest_budget_optimization(self):
        """建議預算優化"""
        today = datetime.now().date()
        current_month_summary = self.transaction_service.get_monthly_summary(
            today.year, today.month
        )
        
        # 如果支出超過收入
        if current_month_summary['net_amount'] < 0:
            deficit = abs(current_month_summary['net_amount'])
            return {
                'type': 'action',
                'icon': '💡',
                'title': '預算優化建議',
                'message': f'本月赤字 ${deficit:.2f}，建議減少非必要支出或增加收入來源'
            }
        
        return None
    
    def _suggest_category_optimization(self):
        """建議類別優化"""
        suggestions = []
        today = datetime.now().date()
        
        # 獲取本月類別統計
        category_stats = self.transaction_service.get_monthly_category_stats(
            today.year, today.month
        )
        
        if not category_stats['expense']:
            return suggestions
        
        # 計算總支出
        total_expense = sum(cat['amount'] for cat in category_stats['expense'])
        
        if total_expense == 0:
            return suggestions
        
        # 找出佔比最高的類別
        sorted_categories = sorted(
            category_stats['expense'],
            key=lambda x: x['amount'],
            reverse=True
        )
        
        # 檢查前三大支出類別
        for i, cat in enumerate(sorted_categories[:3]):
            percentage = (cat['amount'] / total_expense) * 100
            
            # 如果某類別佔比過高（超過 40%）
            if percentage > 40:
                suggestions.append({
                    'type': 'warning',
                    'icon': '📊',
                    'title': f'「{cat["category"]}」支出佔比過高',
                    'message': f'佔總支出的 {percentage:.1f}%，建議檢視是否可以節省'
                })
        
        return suggestions
    
    def _suggest_savings_improvement(self):
        """建議提高儲蓄"""
        today = datetime.now().date()
        summary = self.transaction_service.get_monthly_summary(
            today.year, today.month
        )
        
        if summary['total_income'] == 0:
            return None
        
        savings_rate = (summary['net_amount'] / summary['total_income']) * 100
        
        # 如果儲蓄率低於 20%
        if 0 < savings_rate < 20:
            target_savings = summary['total_income'] * 0.20
            needed_reduction = target_savings - summary['net_amount']
            
            return {
                'type': 'action',
                'icon': '💰',
                'title': '提高儲蓄建議',
                'message': f'目前儲蓄率 {savings_rate:.1f}%，建議減少 ${needed_reduction:.2f} 支出以達到 20% 儲蓄率'
            }
        
        return None
    
    def _suggest_goal_adjustments(self):
        """建議目標調整"""
        suggestions = []
        
        # 獲取所有目標摘要
        goals_summary = self.goal_service.get_all_active_goals_summary()
        
        # 如果沒有設定任何目標
        if goals_summary['total_goals'] == 0:
            suggestions.append({
                'type': 'info',
                'icon': '🎯',
                'title': '建立財務目標',
                'message': '尚未設定任何財務目標，建議設定儲蓄或支出控制目標'
            })
        
        # 如果有很多目標落後
        elif goals_summary['behind'] > goals_summary['on_track']:
            suggestions.append({
                'type': 'warning',
                'icon': '⚠️',
                'title': '多個目標進度落後',
                'message': f'有 {goals_summary["behind"]} 個目標進度落後，建議重新評估目標或調整金額'
            })
        
        # 如果有過期目標
        if goals_summary['overdue'] > 0:
            suggestions.append({
                'type': 'warning',
                'icon': '⏰',
                'title': '目標已過期',
                'message': f'有 {goals_summary["overdue"]} 個目標已過期，建議更新或取消'
            })
        
        return suggestions
    
    def generate_spending_report(self):
        """生成詳細的支出分析報告"""
        today = datetime.now().date()
        
        # 獲取最近 6 個月的資料
        monthly_data = []
        for i in range(6):
            month_offset = i
            if today.month - month_offset < 1:
                year = today.year - ((month_offset - today.month + 1) // 12 + 1)
                month = 12 - ((month_offset - today.month) % 12)
            else:
                year = today.year
                month = today.month - month_offset
            
            summary = self.transaction_service.get_monthly_summary(year, month)
            category_stats = self.transaction_service.get_monthly_category_stats(year, month)
            
            monthly_data.append({
                'year': year,
                'month': month,
                'summary': summary,
                'categories': category_stats
            })
        
        monthly_data.reverse()  # 從舊到新排序
        
        # 計算趨勢
        expenses = [m['summary']['total_expense'] for m in monthly_data]
        avg_expense = sum(expenses) / len(expenses) if expenses else 0
        
        # 找出最常見的高支出類別
        all_expense_categories = {}
        for month_data in monthly_data:
            for cat in month_data['categories']['expense']:
                cat_name = cat['category']
                if cat_name not in all_expense_categories:
                    all_expense_categories[cat_name] = []
                all_expense_categories[cat_name].append(cat['amount'])
        
        # 計算每個類別的平均支出
        category_averages = {
            cat: sum(amounts) / len(amounts)
            for cat, amounts in all_expense_categories.items()
        }
        
        top_categories = sorted(
            category_averages.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            'monthly_data': monthly_data,
            'average_monthly_expense': avg_expense,
            'top_expense_categories': [
                {'category': cat, 'average': avg}
                for cat, avg in top_categories
            ],
            'trend': 'increasing' if expenses[-1] > avg_expense * 1.1 else 'decreasing' if expenses[-1] < avg_expense * 0.9 else 'stable'
        }