from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = None


def generate_all_monthly_reports(app):
    """為所有使用者生成上月報表"""
    with app.app_context():
        from models import db, User
        from services.report_service import ReportService
        
        # 計算上個月
        today = datetime.now()
        if today.month == 1:
            last_month_year = today.year - 1
            last_month = 12
        else:
            last_month_year = today.year
            last_month = today.month - 1
        
        logger.info(f"開始生成 {last_month_year} 年 {last_month} 月的月報表...")
        
        # 獲取所有使用者
        users = User.query.all()
        success_count = 0
        error_count = 0
        
        for user in users:
            try:
                report_service = ReportService(user.id)
                report = report_service.generate_monthly_report(last_month_year, last_month)
                
                if report:
                    logger.info(f"使用者 {user.username} 的月報表已生成")
                    success_count += 1
                else:
                    logger.info(f"使用者 {user.username} 在 {last_month_year}-{last_month} 無交易記錄")
            
            except Exception as e:
                logger.error(f"生成使用者 {user.username} 的月報表時發生錯誤: {e}")
                error_count += 1
        
        logger.info(f"月報表生成完成。成功: {success_count}, 失敗: {error_count}")


def update_all_goals(app):
    """更新所有使用者的目標進度"""
    with app.app_context():
        from models import db, User, Goal
        from services.goal_service import GoalService
        
        logger.info("開始更新所有目標進度...")
        
        # 獲取所有使用者
        users = User.query.all()
        total_goals_updated = 0
        
        for user in users:
            try:
                goal_service = GoalService(user.id)
                
                # 獲取使用者的所有進行中目標
                active_goals = Goal.query.filter_by(
                    user_id=user.id,
                    status='active'
                ).all()
                
                for goal in active_goals:
                    goal_service.update_goal_progress(goal.id)
                    
                    # 檢查是否達成
                    if goal.current_amount >= goal.target_amount:
                        goal.status = 'completed'
                        logger.info(f"目標 {goal.name} 已達成！")
                    
                    total_goals_updated += 1
                
                db.session.commit()
            
            except Exception as e:
                db.session.rollback()
                logger.error(f"更新使用者 {user.username} 的目標時發生錯誤: {e}")
        
        logger.info(f"目標更新完成。共更新 {total_goals_updated} 個目標")


def init_scheduler(app):
    """初始化排程器"""
    global scheduler
    
    if scheduler is not None:
        return scheduler
    
    scheduler = BackgroundScheduler(timezone='Asia/Taipei')
    
    # 每月 1 日凌晨 00:05 自動生成上月報表
    scheduler.add_job(
        func=lambda: generate_all_monthly_reports(app),
        trigger=CronTrigger(day=1, hour=0, minute=5),
        id='monthly_report_job',
        name='生成月報表',
        replace_existing=True
    )
    logger.info("已設定每月報表生成任務：每月 1 日 00:05")
    
    # 每日凌晨 01:00 更新所有目標進度
    scheduler.add_job(
        func=lambda: update_all_goals(app),
        trigger=CronTrigger(hour=1, minute=0),
        id='daily_goal_update_job',
        name='更新目標進度',
        replace_existing=True
    )
    logger.info("已設定每日目標更新任務：每日 01:00")
    
    # 啟動排程器
    scheduler.start()
    logger.info("排程器已啟動")
    
    return scheduler


def shutdown_scheduler():
    """關閉排程器"""
    global scheduler
    
    if scheduler is not None:
        scheduler.shutdown()
        logger.info("排程器已關閉")
        scheduler = None