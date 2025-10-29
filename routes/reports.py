from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, MonthlyReport
from services.report_service import ReportService
from datetime import datetime

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


@reports_bp.route('/')
@login_required
def index():
    """報表列表頁面"""
    # 獲取年份和月份參數
    current_date = datetime.now()
    year = request.args.get('year', current_date.year, type=int)
    month = request.args.get('month', type=int)
    
    # 獲取使用者的所有報表
    reports_query = MonthlyReport.query.filter_by(user_id=current_user.id)
    
    # 如果指定了年份，則篩選
    if year:
        reports_query = reports_query.filter_by(year=year)
    
    # 按年月降序排列
    reports = reports_query.order_by(
        MonthlyReport.year.desc(),
        MonthlyReport.month.desc()
    ).all()
    
    # 獲取所有可用的年份供篩選
    available_years = db.session.query(
        MonthlyReport.year
    ).filter_by(user_id=current_user.id).distinct().order_by(
        MonthlyReport.year.desc()
    ).all()
    available_years = [y[0] for y in available_years]
    
    # 如果指定了月份，則顯示該月的詳細報表
    if month:
        return redirect(url_for('reports.detail', year=year, month=month))
    
    return render_template(
        'reports/index.html',
        reports=reports,
        available_years=available_years,
        current_year=year
    )


@reports_bp.route('/detail/<int:year>/<int:month>')
@login_required
def detail(year, month):
    """月報表詳情頁面"""
    # 驗證月份
    if month < 1 or month > 12:
        flash('無效的月份', 'danger')
        return redirect(url_for('reports.index'))
    
    # 查找報表
    report = MonthlyReport.query.filter_by(
        user_id=current_user.id,
        year=year,
        month=month
    ).first()
    
    # 如果報表不存在，嘗試生成
    if not report:
        report_service = ReportService(current_user.id)
        report = report_service.generate_monthly_report(year, month)
        
        if not report:
            flash(f'{year} 年 {month} 月尚無交易記錄', 'info')
            return redirect(url_for('reports.index'))
    
    # 解析報表資料
    report_data = report.report_data or {}
    
    return render_template(
        'reports/detail.html',
        report=report,
        report_data=report_data,
        year=year,
        month=month
    )


@reports_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    """手動生成月報表"""
    year = request.form.get('year', type=int)
    month = request.form.get('month', type=int)
    
    if not year or not month or month < 1 or month > 12:
        flash('請選擇有效的年份和月份', 'danger')
        return redirect(url_for('reports.index'))
    
    try:
        report_service = ReportService(current_user.id)
        report = report_service.generate_monthly_report(year, month)
        
        if report:
            flash(f'{year} 年 {month} 月的報表已生成', 'success')
            return redirect(url_for('reports.detail', year=year, month=month))
        else:
            flash(f'{year} 年 {month} 月沒有交易記錄', 'info')
            return redirect(url_for('reports.index'))
    
    except Exception as e:
        flash('生成報表失敗，請稍後再試', 'danger')
        print(f"生成報表錯誤: {e}")
        return redirect(url_for('reports.index'))


@reports_bp.route('/regenerate/<int:year>/<int:month>', methods=['POST'])
@login_required
def regenerate(year, month):
    """重新生成月報表"""
    try:
        # 刪除舊報表
        old_report = MonthlyReport.query.filter_by(
            user_id=current_user.id,
            year=year,
            month=month
        ).first()
        
        if old_report:
            db.session.delete(old_report)
            db.session.commit()
        
        # 生成新報表
        report_service = ReportService(current_user.id)
        report = report_service.generate_monthly_report(year, month)
        
        if report:
            flash(f'{year} 年 {month} 月的報表已重新生成', 'success')
        else:
            flash(f'{year} 年 {month} 月沒有交易記錄', 'info')
    
    except Exception as e:
        db.session.rollback()
        flash('重新生成報表失敗，請稍後再試', 'danger')
        print(f"重新生成報表錯誤: {e}")
    
    return redirect(url_for('reports.detail', year=year, month=month))


@reports_bp.route('/compare')
@login_required
def compare():
    """報表比較頁面"""
    # 獲取比較參數
    year1 = request.args.get('year1', type=int)
    month1 = request.args.get('month1', type=int)
    year2 = request.args.get('year2', type=int)
    month2 = request.args.get('month2', type=int)
    
    # 如果沒有提供參數，使用預設值（當月和上月）
    if not all([year1, month1, year2, month2]):
        current_date = datetime.now()
        year1 = current_date.year
        month1 = current_date.month
        
        # 計算上個月
        if month1 == 1:
            year2 = year1 - 1
            month2 = 12
        else:
            year2 = year1
            month2 = month1 - 1
    
    # 獲取兩個報表
    report1 = MonthlyReport.query.filter_by(
        user_id=current_user.id,
        year=year1,
        month=month1
    ).first()
    
    report2 = MonthlyReport.query.filter_by(
        user_id=current_user.id,
        year=year2,
        month=month2
    ).first()
    
    # 如果報表不存在，嘗試生成
    report_service = ReportService(current_user.id)
    
    if not report1:
        report1 = report_service.generate_monthly_report(year1, month1)
    
    if not report2:
        report2 = report_service.generate_monthly_report(year2, month2)
    
    # 計算比較資料
    comparison = None
    if report1 and report2:
        comparison = {
            'income_change': float(report1.total_income - report2.total_income),
            'income_change_percent': calculate_percent_change(
                float(report2.total_income),
                float(report1.total_income)
            ),
            'expense_change': float(report1.total_expense - report2.total_expense),
            'expense_change_percent': calculate_percent_change(
                float(report2.total_expense),
                float(report1.total_expense)
            ),
            'net_change': float(report1.net_amount - report2.net_amount),
            'net_change_percent': calculate_percent_change(
                float(report2.net_amount),
                float(report1.net_amount)
            )
        }
    
    # 獲取所有可用的年月供選擇
    available_months = db.session.query(
        MonthlyReport.year,
        MonthlyReport.month
    ).filter_by(user_id=current_user.id).order_by(
        MonthlyReport.year.desc(),
        MonthlyReport.month.desc()
    ).all()
    
    return render_template(
        'reports/compare.html',
        report1=report1,
        report2=report2,
        year1=year1,
        month1=month1,
        year2=year2,
        month2=month2,
        comparison=comparison,
        available_months=available_months
    )


@reports_bp.route('/summary')
@login_required
def summary():
    """年度總結報表"""
    year = request.args.get('year', datetime.now().year, type=int)
    
    # 獲取該年度的所有月報表
    monthly_reports = MonthlyReport.query.filter_by(
        user_id=current_user.id,
        year=year
    ).order_by(MonthlyReport.month).all()
    
    # 計算年度統計
    yearly_stats = {
        'total_income': sum(float(r.total_income) for r in monthly_reports),
        'total_expense': sum(float(r.total_expense) for r in monthly_reports),
        'net_amount': sum(float(r.net_amount) for r in monthly_reports),
        'avg_monthly_income': 0,
        'avg_monthly_expense': 0,
        'months_with_data': len(monthly_reports)
    }
    
    if yearly_stats['months_with_data'] > 0:
        yearly_stats['avg_monthly_income'] = yearly_stats['total_income'] / yearly_stats['months_with_data']
        yearly_stats['avg_monthly_expense'] = yearly_stats['total_expense'] / yearly_stats['months_with_data']
    
    # 獲取所有可用的年份
    available_years = db.session.query(
        MonthlyReport.year
    ).filter_by(user_id=current_user.id).distinct().order_by(
        MonthlyReport.year.desc()
    ).all()
    available_years = [y[0] for y in available_years]
    
    return render_template(
        'reports/summary.html',
        year=year,
        monthly_reports=monthly_reports,
        yearly_stats=yearly_stats,
        available_years=available_years
    )


@reports_bp.route('/export/<int:year>/<int:month>')
@login_required
def export(year, month):
    """匯出報表為 JSON（供未來擴展）"""
    report = MonthlyReport.query.filter_by(
        user_id=current_user.id,
        year=year,
        month=month
    ).first_or_404()
    
    return jsonify({
        'year': report.year,
        'month': report.month,
        'total_income': float(report.total_income),
        'total_expense': float(report.total_expense),
        'net_amount': float(report.net_amount),
        'report_data': report.report_data
    })


def calculate_percent_change(old_value, new_value):
    """計算百分比變化"""
    if old_value == 0:
        return 100 if new_value > 0 else 0
    return ((new_value - old_value) / abs(old_value)) * 100