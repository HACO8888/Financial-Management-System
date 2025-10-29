"""
資料庫初始化腳本
執行此腳本以建立資料表和初始化預設資料
"""
from app import create_app
from models import db, User, Category
from config import Config


def init_database():
    """初始化資料庫"""
    app = create_app('development')
    
    with app.app_context():
        print("🗄️  開始初始化資料庫...")
        
        # 建立所有資料表
        db.create_all()
        print("✅ 資料表建立完成")
        
        # 檢查是否已有測試使用者
        test_user = User.query.filter_by(username='test').first()
        
        if not test_user:
            # 建立測試使用者
            test_user = User(
                username='test',
                email='test@example.com'
            )
            test_user.set_password('test123')
            db.session.add(test_user)
            db.session.commit()
            print("✅ 測試使用者建立完成 (帳號: test, 密碼: test123)")
            
            # 為測試使用者建立預設類別
            create_default_categories(test_user.id)
            print("✅ 預設類別建立完成")
        else:
            print("ℹ️  測試使用者已存在，跳過建立")
        
        print("🎉 資料庫初始化完成！")
        print("\n📝 測試帳號資訊：")
        print("   帳號: test")
        print("   密碼: test123")
        print("\n🌐 請執行 'python app.py' 啟動應用程式")


def create_default_categories(user_id):
    """建立預設收支類別"""
    # 預設收入類別
    income_categories = Config.DEFAULT_INCOME_CATEGORIES
    for cat_name in income_categories:
        category = Category(
            user_id=user_id,
            name=cat_name,
            type='income',
            is_default=True
        )
        db.session.add(category)
    
    # 預設支出類別
    expense_categories = Config.DEFAULT_EXPENSE_CATEGORIES
    for cat_name in expense_categories:
        category = Category(
            user_id=user_id,
            name=cat_name,
            type='expense',
            is_default=True
        )
        db.session.add(category)
    
    db.session.commit()


if __name__ == '__main__':
    init_database()