from models import db, MonthlyReport, Transaction, Category, Goal
from services.transaction_service import TransactionService
from datetime import datetime
from decimal import Decimal


class ReportService:
    """報表服務"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.transaction_service = TransactionService(user_id)
    
    def generate_monthly_report(self, year, month):
        """生成月報表"""
        # 檢查是否已存在報表
        existing_report = MonthlyReport.query.filter_by(
            user_id=self.user_id,
            year=year,
            month=month
        ).first()
        
        # 如果已存在，先刪除
        if existing_report:
            db.session.delete(existing_report)
            db.session.commit()
        
        # 獲取月度摘要
        summary = self.transaction_service.get_monthly_summary(year, month)
        
        # 如果沒有任何交易，返回 None
        if summary['total_count'] == 0:
            return None
        
        # 獲取詳細資料
        category_stats = self.transaction_service.get_monthly_category_stats(year, month)
        daily_stats = self.transaction_service.get_daily_stats(year, month)
        top_expenses = self.transaction_service.get_top_expenses(year, month)
        weekday_stats = self.transaction_service.get_spending_by_weekday(year, month)
        
        # 獲取目標相關資料
        goals_data = self._get_monthly_goals_data(year, month)
        
        # 計算同比、環比資料
        comparison_data = self._calculate_comparison(year, month)
        
        # 組織報表資料
        report_data = {
            'summary': summary,
            'category_stats': category_stats,
            'daily_stats': daily_stats,
            'top_expenses': top_expenses,
            'weekday_stats': weekday_stats,
            'goals': goals_data,
            'comparison': comparison_data,
            'insights': self._generate_insights(summary, category_stats, comparison_data)
        }
        
        # 建立報表記錄
        report = MonthlyReport(
            user_id=self.user_id,
            year=year,
            month=month,
            total_income=Decimal(str(summary['total_income'])),
            total_expense=Decimal(str(summary['total_expense'])),
            net_amount=Decimal(str(summary['net_amount'])),
            report_data=report_data
        )
        
        db.session.add(report)
        db.session.commit()
        
        return report
    
    def _get_monthly_goals_data(self, year, month):
        """獲取月份相關的目標資料"""
        from calendar import monthrange
        from datetime import date
        
        last_day = monthrange(year, month)[1]
        month_start = date(year, month, 1)
        month_end = date(year, month, last_day)
        
        # 找出在此月份有效的目標
        goals = Goal.query.filter(
            Goal.user_id == self.user_id,
            Goal.start_date <= month_end,
            db.or_(
                Goal.end_date >= month_start,
                Goal.end_date == None
            )
        ).all()
        
        goals_data = []
        for goal in goals:
            goals_data.append({
                'name': goal.name,
                'type': goal.goal_type,
                'target_amount': float(goal.target_amount),
                'current_amount': float(goal.current_amount),
                'progress': goal.calculate_progress(),
                'status': goal.status
            })
        
        return goals_data
    
    def _calculate_comparison(self, year, month):
        """計算同比和環比資料"""
        # 獲取當月資料
        current_summary = self.transaction_service.get_monthly_summary(year, month)
        
        # 計算上月
        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1
        
        # 計算去年同月
        last_year = year - 1
        last_year_month = month
        
        # 獲取上月資料（環比）
        prev_summary = self.transaction_service.get_monthly_summary(prev_year, prev_month)
        
        # 獲取去年同月資料（同比）
        yoy_summary = self.transaction_service.get_monthly_summary(last_year, last_year_month)
        
        def calculate_change(old_val, new_val):
            """計算變化率"""
            if old_val == 0:
                return 0 if new_val == 0 else 100
            return ((new_val - old_val) / old_val) * 100
        
        comparison = {
            'month_over_month': {
                'income_change': calculate_change(
                    prev_summary['total_income'],
                    current_summary['total_income']
                ),
                'expense_change': calculate_change(
                    prev_summary['total_expense'],
                    current_summary['total_expense']
                ),
                'net_change': calculate_change(
                    abs(prev_summary['net_amount']),
                    abs(current_summary['net_amount'])
                )
            },
            'year_over_year': {
                'income_change': calculate_change(
                    yoy_summary['total_income'],
                    current_summary['total_income']
                ),
                'expense_change': calculate_change(
                    yoy_summary['total_expense'],
                    current_summary['total_expense']
                ),
                'net_change': calculate_change(
                    abs(yoy_summary['net_amount']),
                    abs(current_summary['net_amount'])
                )
            }
        }
        
        return comparison
    
    def _generate_insights(self, summary, category_stats, comparison):
        """生成分析見解"""
        insights = []
        
        # 收支平衡分析
        if summary['net_amount'] > 0:
            insights.append({
                'type': 'positive',
                'message': f'本月收支平衡良好，淨收入 ${summary["net_amount"]:.2f}'
            })
        elif summary['net_amount'] < 0:
            insights.append({
                'type': 'warning',
                'message': f'本月支出大於收入，赤字 ${abs(summary["net_amount"]):.2f}'
            })
        else:
            insights.append({
                'type': 'neutral',
                'message': '本月收支平衡'
            })
        
        # 環比分析
        mom_expense_change = comparison['month_over_month']['expense_change']
        if mom_expense_change > 20:
            insights.append({
                'type': 'warning',
                'message': f'本月支出較上月增加 {mom_expense_change:.1f}%，請注意控制'
            })
        elif mom_expense_change < -20:
            insights.append({
                'type': 'positive',
                'message': f'本月支出較上月減少 {abs(mom_expense_change):.1f}%，值得表揚！'
            })
        
        # 類別分析 - 找出最大支出類別
        if category_stats['expense']:
            max_expense_cat = max(category_stats['expense'], key=lambda x: x['amount'])
            total_expense = sum(cat['amount'] for cat in category_stats['expense'])
            
            if total_expense > 0:
                percentage = (max_expense_cat['amount'] / total_expense) * 100
                if percentage > 40:
                    insights.append({
                        'type': 'info',
                        'message': f'「{max_expense_cat["category"]}」佔總支出的 {percentage:.1f}%，為最大支出項目'
                    })
        
        # 儲蓄率分析
        if summary['total_income'] > 0:
            savings_rate = (summary['net_amount'] / summary['total_income']) * 100
            
            if savings_rate >= 30:
                insights.append({
                    'type': 'positive',
                    'message': f'儲蓄率達 {savings_rate:.1f}%，表現優異！'
                })
            elif savings_rate >= 20:
                insights.append({
                    'type': 'positive',
                    'message': f'儲蓄率為 {savings_rate:.1f}%，保持良好習慣'
                })
            elif savings_rate >= 10:
                insights.append({
                    'type': 'info',
                    'message': f'儲蓄率為 {savings_rate:.1f}%，仍有改善空間'
                })
            elif savings_rate > 0:
                insights.append({
                    'type': 'warning',
                    'message': f'儲蓄率僅 {savings_rate:.1f}%，建議提高儲蓄比例'
                })
            else:
                insights.append({
                    'type': 'warning',
                    'message': '本月無儲蓄，建議檢視支出並調整預算'
                })
        
        return insights
    
    def get_yearly_summary(self, year):
        """獲取年度總結"""
        # 獲取該年度的所有月報表
        monthly_reports = MonthlyReport.query.filter_by(
            user_id=self.user_id,
            year=year
        ).order_by(MonthlyReport.month).all()
        
        if not monthly_reports:
            return None
        
        # 計算年度統計
        total_income = sum(float(r.total_income) for r in monthly_reports)
        total_expense = sum(float(r.total_expense) for r in monthly_reports)
        net_amount = total_income - total_expense
        
        # 計算月均
        months_count = len(monthly_reports)
        avg_monthly_income = total_income / months_count
        avg_monthly_expense = total_expense / months_count
        
        # 找出收入和支出最高的月份
        max_income_month = max(monthly_reports, key=lambda r: r.total_income)
        max_expense_month = max(monthly_reports, key=lambda r: r.total_expense)
        
        # 計算儲蓄率
        savings_rate = (net_amount / total_income * 100) if total_income > 0 else 0
        
        return {
            'year': year,
            'total_income': total_income,
            'total_expense': total_expense,
            'net_amount': net_amount,
            'avg_monthly_income': avg_monthly_income,
            'avg_monthly_expense': avg_monthly_expense,
            'months_with_data': months_count,
            'max_income_month': max_income_month.month,
            'max_income_amount': float(max_income_month.total_income),
            'max_expense_month': max_expense_month.month,
            'max_expense_amount': float(max_expense_month.total_expense),
            'savings_rate': savings_rate,
            'monthly_reports': monthly_reports
        }
    
    def get_category_yearly_breakdown(self, year):
        """獲取年度類別明細"""
        from datetime import date
        from calendar import monthrange
        
        start_date = date(year, 1, 1)
        last_day = monthrange(year, 12)[1]
        end_date = date(year, 12, last_day)
        
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


from sqlalchemy import func