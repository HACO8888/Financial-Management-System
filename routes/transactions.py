from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Transaction, Category
from services.transaction_service import TransactionService
from datetime import datetime, timedelta
from decimal import Decimal

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')


@transactions_bp.route('/')
@login_required
def index():
    """交易列表頁面"""
    # 獲取篩選參數
    transaction_type = request.args.get('type', 'all')  # all, income, expense
    category_id = request.args.get('category', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 建立查詢
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    # 應用篩選條件
    if transaction_type != 'all':
        query = query.filter_by(type=transaction_type)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Transaction.date >= start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Transaction.date <= end)
        except ValueError:
            pass
    
    # 排序和分頁
    transactions = query.order_by(
        Transaction.date.desc(), 
        Transaction.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    # 獲取所有類別供篩選使用
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.type, Category.name).all()
    
    # 計算篩選結果的統計
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'income'
    )
    if start_date:
        total_income = total_income.filter(Transaction.date >= start)
    if end_date:
        total_income = total_income.filter(Transaction.date <= end)
    total_income = total_income.scalar() or 0
    
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense'
    )
    if start_date:
        total_expense = total_expense.filter(Transaction.date >= start)
    if end_date:
        total_expense = total_expense.filter(Transaction.date <= end)
    total_expense = total_expense.scalar() or 0
    
    return render_template(
        'transactions/index.html',
        transactions=transactions,
        categories=categories,
        filters={
            'type': transaction_type,
            'category': category_id,
            'start_date': start_date,
            'end_date': end_date
        },
        total_income=total_income,
        total_expense=total_expense
    )


@transactions_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """新增交易"""
    if request.method == 'POST':
        transaction_type = request.form.get('type')
        category_id = request.form.get('category_id', type=int)
        amount = request.form.get('amount')
        date_str = request.form.get('date')
        description = request.form.get('description', '').strip()
        
        # 驗證輸入
        errors = []
        
        if not transaction_type or transaction_type not in ['income', 'expense']:
            errors.append('請選擇交易類型')
        
        if not category_id:
            errors.append('請選擇類別')
        else:
            # 驗證類別是否屬於當前使用者
            category = Category.query.filter_by(
                id=category_id, 
                user_id=current_user.id
            ).first()
            if not category:
                errors.append('無效的類別')
            elif category.type != transaction_type:
                errors.append('類別類型與交易類型不符')
        
        if not amount:
            errors.append('請輸入金額')
        else:
            try:
                amount = Decimal(amount)
                if amount <= 0:
                    errors.append('金額必須大於 0')
            except:
                errors.append('請輸入有效的金額')
        
        if not date_str:
            errors.append('請選擇日期')
        else:
            try:
                transaction_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('日期格式錯誤')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            # 獲取類別供重新顯示表單
            categories = Category.query.filter_by(user_id=current_user.id).order_by(
                Category.type, Category.name
            ).all()
            return render_template('transactions/add.html', categories=categories)
        
        # 建立交易記錄
        try:
            transaction = Transaction(
                user_id=current_user.id,
                category_id=category_id,
                type=transaction_type,
                amount=amount,
                date=transaction_date,
                description=description
            )
            db.session.add(transaction)
            db.session.commit()
            
            # 更新相關目標進度
            transaction_service = TransactionService(current_user.id)
            transaction_service.update_goals_progress()
            
            flash('交易記錄已成功新增', 'success')
            return redirect(url_for('transactions.index'))
        
        except Exception as e:
            db.session.rollback()
            flash('新增失敗，請稍後再試', 'danger')
            print(f"新增交易錯誤: {e}")
    
    # GET 請求：顯示表單
    categories = Category.query.filter_by(user_id=current_user.id).order_by(
        Category.type, Category.name
    ).all()
    
    return render_template('transactions/add.html', categories=categories)


@transactions_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """編輯交易"""
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        amount = request.form.get('amount')
        date_str = request.form.get('date')
        description = request.form.get('description', '').strip()
        
        # 驗證輸入
        errors = []
        
        if not category_id:
            errors.append('請選擇類別')
        else:
            category = Category.query.filter_by(
                id=category_id,
                user_id=current_user.id,
                type=transaction.type
            ).first()
            if not category:
                errors.append('無效的類別')
        
        if not amount:
            errors.append('請輸入金額')
        else:
            try:
                amount = Decimal(amount)
                if amount <= 0:
                    errors.append('金額必須大於 0')
            except:
                errors.append('請輸入有效的金額')
        
        if not date_str:
            errors.append('請選擇日期')
        else:
            try:
                transaction_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('日期格式錯誤')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
        else:
            # 更新交易記錄
            try:
                transaction.category_id = category_id
                transaction.amount = amount
                transaction.date = transaction_date
                transaction.description = description
                db.session.commit()
                
                # 更新相關目標進度
                transaction_service = TransactionService(current_user.id)
                transaction_service.update_goals_progress()
                
                flash('交易記錄已更新', 'success')
                return redirect(url_for('transactions.index'))
            
            except Exception as e:
                db.session.rollback()
                flash('更新失敗，請稍後再試', 'danger')
                print(f"編輯交易錯誤: {e}")
    
    # GET 請求：顯示編輯表單
    categories = Category.query.filter_by(
        user_id=current_user.id,
        type=transaction.type
    ).order_by(Category.name).all()
    
    return render_template('transactions/edit.html', transaction=transaction, categories=categories)


@transactions_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """刪除交易"""
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(transaction)
        db.session.commit()
        
        # 更新相關目標進度
        transaction_service = TransactionService(current_user.id)
        transaction_service.update_goals_progress()
        
        flash('交易記錄已刪除', 'success')
    except Exception as e:
        db.session.rollback()
        flash('刪除失敗，請稍後再試', 'danger')
        print(f"刪除交易錯誤: {e}")
    
    return redirect(url_for('transactions.index'))


@transactions_bp.route('/categories')
@login_required
def categories():
    """類別管理頁面"""
    income_categories = Category.query.filter_by(
        user_id=current_user.id,
        type='income'
    ).order_by(Category.is_default.desc(), Category.name).all()
    
    expense_categories = Category.query.filter_by(
        user_id=current_user.id,
        type='expense'
    ).order_by(Category.is_default.desc(), Category.name).all()
    
    return render_template(
        'transactions/categories.html',
        income_categories=income_categories,
        expense_categories=expense_categories
    )


@transactions_bp.route('/categories/add', methods=['POST'])
@login_required
def add_category():
    """新增自訂類別"""
    name = request.form.get('name', '').strip()
    category_type = request.form.get('type')
    
    if not name or not category_type or category_type not in ['income', 'expense']:
        flash('請輸入有效的類別名稱和類型', 'danger')
        return redirect(url_for('transactions.categories'))
    
    # 檢查是否已存在同名類別
    existing = Category.query.filter_by(
        user_id=current_user.id,
        name=name,
        type=category_type
    ).first()
    
    if existing:
        flash('此類別名稱已存在', 'warning')
        return redirect(url_for('transactions.categories'))
    
    try:
        category = Category(
            user_id=current_user.id,
            name=name,
            type=category_type,
            is_default=False
        )
        db.session.add(category)
        db.session.commit()
        flash('類別已新增', 'success')
    except Exception as e:
        db.session.rollback()
        flash('新增失敗，請稍後再試', 'danger')
        print(f"新增類別錯誤: {e}")
    
    return redirect(url_for('transactions.categories'))


@transactions_bp.route('/categories/delete/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    """刪除自訂類別"""
    category = Category.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # 不允許刪除預設類別
    if category.is_default:
        flash('不能刪除預設類別', 'warning')
        return redirect(url_for('transactions.categories'))
    
    # 檢查是否有交易使用此類別
    transaction_count = Transaction.query.filter_by(category_id=id).count()
    if transaction_count > 0:
        flash(f'此類別已被 {transaction_count} 筆交易使用，無法刪除', 'warning')
        return redirect(url_for('transactions.categories'))
    
    try:
        db.session.delete(category)
        db.session.commit()
        flash('類別已刪除', 'success')
    except Exception as e:
        db.session.rollback()
        flash('刪除失敗，請稍後再試', 'danger')
        print(f"刪除類別錯誤: {e}")
    
    return redirect(url_for('transactions.categories'))