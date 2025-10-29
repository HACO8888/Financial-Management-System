import re
from datetime import datetime
from decimal import Decimal, InvalidOperation


def validate_email(email):
    """驗證電子郵件格式"""
    if not email:
        return False, "電子郵件不能為空"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "電子郵件格式不正確"
    
    return True, ""


def validate_username(username):
    """驗證使用者名稱"""
    if not username:
        return False, "使用者名稱不能為空"
    
    if len(username) < 3:
        return False, "使用者名稱至少需要 3 個字元"
    
    if len(username) > 80:
        return False, "使用者名稱不能超過 80 個字元"
    
    # 只允許字母、數字、底線和連字號
    pattern = r'^[a-zA-Z0-9_-]+$'
    if not re.match(pattern, username):
        return False, "使用者名稱只能包含字母、數字、底線和連字號"
    
    return True, ""


def validate_password(password):
    """驗證密碼強度"""
    if not password:
        return False, "密碼不能為空"
    
    if len(password) < 6:
        return False, "密碼至少需要 6 個字元"
    
    if len(password) > 128:
        return False, "密碼不能超過 128 個字元"
    
    # 可選：更嚴格的密碼要求
    # has_upper = any(c.isupper() for c in password)
    # has_lower = any(c.islower() for c in password)
    # has_digit = any(c.isdigit() for c in password)
    # 
    # if not (has_upper and has_lower and has_digit):
    #     return False, "密碼必須包含大寫字母、小寫字母和數字"
    
    return True, ""


def validate_amount(amount_str):
    """驗證金額"""
    if not amount_str:
        return False, "金額不能為空", None
    
    try:
        amount = Decimal(str(amount_str))
        
        if amount <= 0:
            return False, "金額必須大於 0", None
        
        if amount > Decimal('9999999999.99'):
            return False, "金額過大", None
        
        # 檢查小數位數（最多 2 位）
        if amount.as_tuple().exponent < -2:
            return False, "金額最多只能有 2 位小數", None
        
        return True, "", amount
    
    except (InvalidOperation, ValueError):
        return False, "金額格式不正確", None


def validate_date(date_str, allow_future=True):
    """驗證日期格式"""
    if not date_str:
        return False, "日期不能為空", None
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # 檢查是否為未來日期
        if not allow_future and date_obj > datetime.now().date():
            return False, "日期不能是未來日期", None
        
        # 檢查日期是否過於久遠（例如：1900 年之前）
        if date_obj.year < 1900:
            return False, "日期過於久遠", None
        
        return True, "", date_obj
    
    except ValueError:
        return False, "日期格式不正確（應為 YYYY-MM-DD）", None


def validate_category_name(name):
    """驗證類別名稱"""
    if not name:
        return False, "類別名稱不能為空"
    
    name = name.strip()
    
    if len(name) < 1:
        return False, "類別名稱不能為空"
    
    if len(name) > 50:
        return False, "類別名稱不能超過 50 個字元"
    
    return True, ""


def validate_goal_name(name):
    """驗證目標名稱"""
    if not name:
        return False, "目標名稱不能為空"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "目標名稱至少需要 2 個字元"
    
    if len(name) > 100:
        return False, "目標名稱不能超過 100 個字元"
    
    return True, ""


def validate_transaction_type(transaction_type):
    """驗證交易類型"""
    valid_types = ['income', 'expense']
    
    if not transaction_type:
        return False, "請選擇交易類型"
    
    if transaction_type not in valid_types:
        return False, "無效的交易類型"
    
    return True, ""


def validate_goal_type(goal_type):
    """驗證目標類型"""
    valid_types = ['saving', 'expense_limit']
    
    if not goal_type:
        return False, "請選擇目標類型"
    
    if goal_type not in valid_types:
        return False, "無效的目標類型"
    
    return True, ""


def validate_period(period):
    """驗證期限類型"""
    valid_periods = ['monthly', 'yearly', 'custom']
    
    if not period:
        return False, "請選擇期限類型"
    
    if period not in valid_periods:
        return False, "無效的期限類型"
    
    return True, ""


def sanitize_string(text, max_length=None):
    """清理字串（移除多餘空白）"""
    if not text:
        return ""
    
    # 移除前後空白
    text = text.strip()
    
    # 移除多餘的空白字元
    text = re.sub(r'\s+', ' ', text)
    
    # 限制長度
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_year_month(year, month):
    """驗證年份和月份"""
    if not year or not month:
        return False, "請提供年份和月份"
    
    try:
        year = int(year)
        month = int(month)
    except (ValueError, TypeError):
        return False, "年份和月份必須是數字"
    
    if year < 1900 or year > 2100:
        return False, "無效的年份"
    
    if month < 1 or month > 12:
        return False, "月份必須在 1-12 之間"
    
    return True, ""


def is_safe_redirect_url(url):
    """檢查重定向 URL 是否安全（防止開放重定向漏洞）"""
    if not url:
        return False
    
    # 只允許相對 URL
    if url.startswith('http://') or url.startswith('https://') or url.startswith('//'):
        return False
    
    # 不允許包含 @（可能用於偽造域名）
    if '@' in url:
        return False
    
    return True