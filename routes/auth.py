from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Category
from config import Config
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登入頁面"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        # 驗證輸入
        if not username or not password:
            flash('請輸入帳號和密碼', 'danger')
            return render_template('auth/login.html')
        
        # 查找使用者
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'歡迎回來，{user.username}！', 'success')
            
            # 重定向到原本要訪問的頁面
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
        else:
            flash('帳號或密碼錯誤', 'danger')
    
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """註冊頁面"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # 驗證輸入
        errors = []
        
        if not username or len(username) < 3:
            errors.append('使用者名稱至少需要 3 個字元')
        
        if not email or '@' not in email:
            errors.append('請輸入有效的電子郵件地址')
        
        if not password or len(password) < 6:
            errors.append('密碼至少需要 6 個字元')
        
        if password != confirm_password:
            errors.append('兩次輸入的密碼不一致')
        
        # 檢查使用者名稱是否已存在
        if User.query.filter_by(username=username).first():
            errors.append('此使用者名稱已被使用')
        
        # 檢查電子郵件是否已存在
        if User.query.filter_by(email=email).first():
            errors.append('此電子郵件已被註冊')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
        
        # 建立新使用者
        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            # 為新使用者建立預設類別
            create_default_categories(new_user.id)
            
            flash('註冊成功！請登入', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            flash('註冊失敗，請稍後再試', 'danger')
            print(f"註冊錯誤: {e}")
    
    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """登出"""
    logout_user()
    flash('已成功登出', 'info')
    return redirect(url_for('auth.login'))


def create_default_categories(user_id):
    """為新使用者建立預設收支類別"""
    try:
        # 建立預設收入類別
        for cat_name in Config.DEFAULT_INCOME_CATEGORIES:
            category = Category(
                user_id=user_id,
                name=cat_name,
                type='income',
                is_default=True
            )
            db.session.add(category)
        
        # 建立預設支出類別
        for cat_name in Config.DEFAULT_EXPENSE_CATEGORIES:
            category = Category(
                user_id=user_id,
                name=cat_name,
                type='expense',
                is_default=True
            )
            db.session.add(category)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"建立預設類別錯誤: {e}")