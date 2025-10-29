from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Goal
from services.goal_service import GoalService
from datetime import datetime, timedelta
from decimal import Decimal
from dateutil.relativedelta import relativedelta

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')


@goals_bp.route('/')
@login_required
def index():
    """目標列表頁面"""
    # 獲取篩選參數
    status_filter = request.args.get('status', 'active')  # active, completed, cancelled, all
    
    # 建立查詢
    query = Goal.query.filter_by(user_id=current_user.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    # 排序：進行中的優先，然後按建立日期
    goals = query.order_by(
        Goal.status == 'active',
        Goal.created_at.desc()
    ).all()
    
    # 計算每個目標的進度
    goal_service = GoalService(current_user.id)
    for goal in goals:
        goal.progress = goal.calculate_progress()
        goal.is_overdue = goal_service.is_goal_overdue(goal)
        
        # 對於進行中的目標，更新當前金額
        if goal.status == 'active':
            goal_service.update_goal_progress(goal.id)
    
    # 統計資料
    total_goals = Goal.query.filter_by(user_id=current_user.id).count()
    active_goals = Goal.query.filter_by(user_id=current_user.id, status='active').count()
    completed_goals = Goal.query.filter_by(user_id=current_user.id, status='completed').count()
    
    return render_template(
        'goals/index.html',
        goals=goals,
        status_filter=status_filter,
        total_goals=total_goals,
        active_goals=active_goals,
        completed_goals=completed_goals
    )


@goals_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """新增目標"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        goal_type = request.form.get('goal_type')
        target_amount = request.form.get('target_amount')
        period = request.form.get('period')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        # 驗證輸入
        errors = []
        
        if not name or len(name) < 2:
            errors.append('目標名稱至少需要 2 個字元')
        
        if not goal_type or goal_type not in ['saving', 'expense_limit']:
            errors.append('請選擇目標類型')
        
        if not target_amount:
            errors.append('請輸入目標金額')
        else:
            try:
                target_amount = Decimal(target_amount)
                if target_amount <= 0:
                    errors.append('目標金額必須大於 0')
            except:
                errors.append('請輸入有效的目標金額')
        
        if not period or period not in ['monthly', 'yearly', 'custom']:
            errors.append('請選擇期限類型')
        
        if not start_date_str:
            errors.append('請選擇開始日期')
        else:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('開始日期格式錯誤')
        
        # 根據期限類型設定結束日期
        if period == 'custom':
            if not end_date_str:
                errors.append('自訂期限需要指定結束日期')
            else:
                try:
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                    if end_date <= start_date:
                        errors.append('結束日期必須晚於開始日期')
                except ValueError:
                    errors.append('結束日期格式錯誤')
        elif period == 'monthly':
            end_date = start_date + relativedelta(months=1) - timedelta(days=1)
        elif period == 'yearly':
            end_date = start_date + relativedelta(years=1) - timedelta(days=1)
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('goals/add.html')
        
        # 建立目標
        try:
            goal = Goal(
                user_id=current_user.id,
                name=name,
                goal_type=goal_type,
                target_amount=target_amount,
                period=period,
                start_date=start_date,
                end_date=end_date,
                status='active'
            )
            db.session.add(goal)
            db.session.commit()
            
            # 立即計算初始進度
            goal_service = GoalService(current_user.id)
            goal_service.update_goal_progress(goal.id)
            
            flash('目標已成功建立', 'success')
            return redirect(url_for('goals.index'))
        
        except Exception as e:
            db.session.rollback()
            flash('建立失敗，請稍後再試', 'danger')
            print(f"新增目標錯誤: {e}")
    
    # GET 請求：顯示表單
    return render_template('goals/add.html')


@goals_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """編輯目標"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        target_amount = request.form.get('target_amount')
        end_date_str = request.form.get('end_date')
        
        # 驗證輸入
        errors = []
        
        if not name or len(name) < 2:
            errors.append('目標名稱至少需要 2 個字元')
        
        if not target_amount:
            errors.append('請輸入目標金額')
        else:
            try:
                target_amount = Decimal(target_amount)
                if target_amount <= 0:
                    errors.append('目標金額必須大於 0')
            except:
                errors.append('請輸入有效的目標金額')
        
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                if end_date <= goal.start_date:
                    errors.append('結束日期必須晚於開始日期')
            except ValueError:
                errors.append('結束日期格式錯誤')
        else:
            end_date = goal.end_date
        
        if errors:
            for error in errors:
                flash(error, 'danger')
        else:
            # 更新目標
            try:
                goal.name = name
                goal.target_amount = target_amount
                goal.end_date = end_date
                db.session.commit()
                
                flash('目標已更新', 'success')
                return redirect(url_for('goals.index'))
            
            except Exception as e:
                db.session.rollback()
                flash('更新失敗，請稍後再試', 'danger')
                print(f"編輯目標錯誤: {e}")
    
    # GET 請求：顯示編輯表單
    return render_template('goals/edit.html', goal=goal)


@goals_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """刪除目標"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(goal)
        db.session.commit()
        flash('目標已刪除', 'success')
    except Exception as e:
        db.session.rollback()
        flash('刪除失敗，請稍後再試', 'danger')
        print(f"刪除目標錯誤: {e}")
    
    return redirect(url_for('goals.index'))


@goals_bp.route('/complete/<int:id>', methods=['POST'])
@login_required
def complete(id):
    """標記目標為已完成"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        goal.status = 'completed'
        db.session.commit()
        flash(f'恭喜！目標「{goal.name}」已完成！', 'success')
    except Exception as e:
        db.session.rollback()
        flash('操作失敗，請稍後再試', 'danger')
        print(f"完成目標錯誤: {e}")
    
    return redirect(url_for('goals.index'))


@goals_bp.route('/cancel/<int:id>', methods=['POST'])
@login_required
def cancel(id):
    """取消目標"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        goal.status = 'cancelled'
        db.session.commit()
        flash('目標已取消', 'info')
    except Exception as e:
        db.session.rollback()
        flash('操作失敗，請稍後再試', 'danger')
        print(f"取消目標錯誤: {e}")
    
    return redirect(url_for('goals.index'))


@goals_bp.route('/reactivate/<int:id>', methods=['POST'])
@login_required
def reactivate(id):
    """重新啟動已取消的目標"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if goal.status != 'cancelled':
        flash('只能重新啟動已取消的目標', 'warning')
        return redirect(url_for('goals.index'))
    
    try:
        goal.status = 'active'
        # 更新開始日期為今天
        goal.start_date = datetime.now().date()
        # 重新計算結束日期
        if goal.period == 'monthly':
            goal.end_date = goal.start_date + relativedelta(months=1) - timedelta(days=1)
        elif goal.period == 'yearly':
            goal.end_date = goal.start_date + relativedelta(years=1) - timedelta(days=1)
        
        db.session.commit()
        
        # 更新進度
        goal_service = GoalService(current_user.id)
        goal_service.update_goal_progress(goal.id)
        
        flash('目標已重新啟動', 'success')
    except Exception as e:
        db.session.rollback()
        flash('操作失敗，請稍後再試', 'danger')
        print(f"重新啟動目標錯誤: {e}")
    
    return redirect(url_for('goals.index'))


@goals_bp.route('/detail/<int:id>')
@login_required
def detail(id):
    """目標詳情頁面"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # 計算進度
    goal.progress = goal.calculate_progress()
    
    # 獲取目標相關的統計資料
    goal_service = GoalService(current_user.id)
    stats = goal_service.get_goal_statistics(goal.id)
    
    return render_template('goals/detail.html', goal=goal, stats=stats)


@goals_bp.route('/refresh-progress', methods=['POST'])
@login_required
def refresh_progress():
    """手動刷新所有目標進度（AJAX 端點）"""
    goal_service = GoalService(current_user.id)
    
    try:
        # 更新所有進行中的目標
        active_goals = Goal.query.filter_by(
            user_id=current_user.id,
            status='active'
        ).all()
        
        for goal in active_goals:
            goal_service.update_goal_progress(goal.id)
            
            # 檢查是否達成目標
            if goal.current_amount >= goal.target_amount:
                goal.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '進度已更新'
        })
    
    except Exception as e:
        db.session.rollback()
        print(f"刷新進度錯誤: {e}")
        return jsonify({
            'success': False,
            'message': '更新失敗'
        }), 500