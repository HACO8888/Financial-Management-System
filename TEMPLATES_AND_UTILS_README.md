# 📂 Utils 和 Templates 檔案說明

## ✅ 已建立的檔案總覽

### 🔧 Utils 資料夾（工具模組）

#### 1. **utils/__init__.py**
- 套件初始化檔案

#### 2. **[utils/scheduler.py](computer:///mnt/user-data/outputs/utils/scheduler.py)** (4.4 KB)
**自動排程任務管理器**
- ✅ 每月 1 日自動生成上月報表
- ✅ 每日自動更新目標進度
- ✅ 使用 APScheduler 排程器
- ✅ 支援啟動和關閉排程器

**主要功能：**
- `generate_all_monthly_reports()` - 為所有使用者生成月報表
- `update_all_goals()` - 更新所有使用者的目標進度
- `init_scheduler()` - 初始化排程器
- `shutdown_scheduler()` - 關閉排程器

#### 3. **[utils/validators.py](computer:///mnt/user-data/outputs/utils/validators.py)** (5.9 KB)
**資料驗證工具集**
- ✅ 電子郵件格式驗證
- ✅ 使用者名稱驗證
- ✅ 密碼強度驗證
- ✅ 金額驗證（小數處理）
- ✅ 日期驗證
- ✅ 類別名稱驗證
- ✅ 目標名稱驗證
- ✅ 安全性檢查（防止開放重定向）

---

### 🎨 Templates 資料夾（前端模板）

#### **基礎模板**

##### 1. **[base.html](computer:///mnt/user-data/outputs/templates/base.html)** (5.4 KB)
**主模板框架**
- ✅ Bootstrap 5 整合
- ✅ 響應式導航欄
- ✅ Flash 訊息顯示
- ✅ Chart.js 圖表支援
- ✅ jQuery 整合

---

#### **登入/註冊模組（auth/）**

##### 2. **[auth/login.html](computer:///mnt/user-data/outputs/templates/auth/login.html)**
**登入頁面**
- ✅ 美觀的登入表單
- ✅ 記住我功能
- ✅ 測試帳號提示

##### 3. **[auth/register.html](computer:///mnt/user-data/outputs/templates/auth/register.html)**
**註冊頁面**
- ✅ 完整的註冊表單
- ✅ 密碼確認欄位
- ✅ 輸入驗證提示

---

#### **儀表板模組（dashboard/）**

##### 4. **[dashboard/index.html](computer:///mnt/user-data/outputs/templates/dashboard/index.html)**
**主儀表板**
- ✅ 本月收支統計卡片
- ✅ 收支分布圖表（Chart.js）
- ✅ 最近交易記錄
- ✅ 進行中的目標顯示
- ✅ 分析見解卡片
- ✅ 理財建議顯示

---

#### **交易管理模組（transactions/）**

##### 5. **[transactions/index.html](computer:///mnt/user-data/outputs/templates/transactions/index.html)**
**交易列表頁**
- ✅ 統計卡片（總收入/支出/淨額）
- ✅ 進階篩選功能（類型、類別、日期範圍）
- ✅ 分頁顯示
- ✅ 編輯/刪除操作

##### 6. **[transactions/add.html](computer:///mnt/user-data/outputs/templates/transactions/add.html)**
**新增交易頁**
- ✅ 收入/支出切換按鈕
- ✅ 動態類別選擇
- ✅ 金額、日期、描述輸入
- ✅ JavaScript 表單增強

##### 7. **[transactions/edit.html](computer:///mnt/user-data/outputs/templates/transactions/edit.html)**
**編輯交易頁**
- ✅ 預填現有資料
- ✅ 類型不可修改提示
- ✅ 表單驗證

##### 8. **[transactions/categories.html](computer:///mnt/user-data/outputs/templates/transactions/categories.html)**
**類別管理頁**
- ✅ 收入/支出類別分開顯示
- ✅ 新增自訂類別
- ✅ 刪除自訂類別（預設類別不可刪）
- ✅ 預設類別標記

---

#### **財務目標模組（goals/）**

##### 9. **[goals/index.html](computer:///mnt/user-data/outputs/templates/goals/index.html)**
**目標列表頁**
- ✅ 目標統計卡片
- ✅ 狀態篩選（進行中/已完成/已取消）
- ✅ 進度條視覺化
- ✅ 目標操作按鈕（編輯/完成/取消/刪除）
- ✅ 過期提示

##### 10. **[goals/add.html](computer:///mnt/user-data/outputs/templates/goals/add.html)**
**新增目標頁**
- ✅ 目標類型選擇（儲蓄/支出限制）
- ✅ 期限類型選擇（每月/每年/自訂）
- ✅ 動態顯示結束日期欄位
- ✅ JavaScript 表單增強

##### 11. **[goals/edit.html](computer:///mnt/user-data/outputs/templates/goals/edit.html)**
**編輯目標頁**
- ✅ 預填現有資料
- ✅ 不可修改欄位提示
- ✅ 當前進度顯示

---

#### **報表模組（reports/）**

##### 12. **[reports/index.html](computer:///mnt/user-data/outputs/templates/reports/index.html)**
**報表列表頁**
- ✅ 年份篩選按鈕
- ✅ 月報表卡片顯示
- ✅ 手動生成報表 Modal
- ✅ 重新生成功能
- ✅ 查看詳情連結

##### 13. **[reports/detail.html](computer:///mnt/user-data/outputs/templates/reports/detail.html)**
**報表詳情頁**
- ✅ 四大統計卡片（收入/支出/淨額/交易數）
- ✅ 類別圓餅圖（Chart.js）
- ✅ 每日趨勢折線圖（Chart.js）
- ✅ 最大支出項目列表
- ✅ 分析見解顯示
- ✅ 環比變化數據
- ✅ 相關目標顯示

---

#### **錯誤頁面模組（errors/）**

##### 14. **[errors/404.html](computer:///mnt/user-data/outputs/templates/errors/404.html)**
**404 錯誤頁**
- ✅ 友善的錯誤提示
- ✅ 返回首頁按鈕

##### 15. **[errors/500.html](computer:///mnt/user-data/outputs/templates/errors/500.html)**
**500 錯誤頁**
- ✅ 伺服器錯誤提示
- ✅ 返回首頁按鈕

---

## 🎯 模板特色功能

### **1. 響應式設計**
- ✅ 使用 Bootstrap 5 框架
- ✅ 支援手機、平板、電腦
- ✅ 流暢的使用者體驗

### **2. 視覺化圖表**
- ✅ Chart.js 整合
- ✅ 圓餅圖、柱狀圖、折線圖
- ✅ 動態資料載入

### **3. 互動功能**
- ✅ 動態表單驗證
- ✅ 即時篩選和搜尋
- ✅ Modal 彈窗
- ✅ Ajax 請求支援

### **4. 使用者體驗**
- ✅ Flash 訊息提示
- ✅ 確認對話框
- ✅ 載入動畫
- ✅ 友善的錯誤提示

### **5. 資料視覺化**
- ✅ 進度條顯示
- ✅ 徽章標籤
- ✅ 圖示系統（Bootstrap Icons）
- ✅ 色彩編碼（收入綠色、支出紅色）

---

## 📝 使用說明

### **啟動排程器**
排程器會在應用程式啟動時自動初始化（在 `app.py` 中）：
```python
from utils.scheduler import init_scheduler
init_scheduler(app)
```

### **使用驗證器**
在路由或服務中使用驗證函數：
```python
from utils.validators import validate_email, validate_amount

is_valid, error_msg = validate_email(email)
if not is_valid:
    flash(error_msg, 'danger')
    
is_valid, error_msg, amount = validate_amount(amount_str)
```

### **模板繼承**
所有頁面都繼承自 `base.html`：
```html
{% extends "base.html" %}

{% block title %}您的頁面標題{% endblock %}

{% block content %}
<!-- 您的內容 -->
{% endblock %}

{% block extra_js %}
<!-- 額外的 JavaScript -->
{% endblock %}
```

---

## 🔍 關鍵設計模式

### **1. 模板區塊系統**
- `title` - 頁面標題
- `extra_css` - 額外 CSS
- `content` - 主要內容
- `extra_js` - 額外 JavaScript

### **2. Flash 訊息類別**
- `success` - 成功（綠色）
- `danger` - 錯誤（紅色）
- `warning` - 警告（黃色）
- `info` - 資訊（藍色）

### **3. 表單設計原則**
- 必填欄位標記 `<span class="text-danger">*</span>`
- 輸入群組使用 Bootstrap 的 `input-group`
- 提示文字使用 `<small class="text-muted">`
- 按鈕操作使用 `d-grid gap-2` 排版

---

## 🚀 下一步

現在已完成 **Utils** 和 **Templates** 的建立！

接下來需要建立：
- **static/** 資料夾（CSS、JavaScript、圖片等靜態資源）

---

**建立時間**: 2025年10月29日  
**檔案總數**: 18 個（3 個 Utils + 15 個 Templates）  
**程式碼總量**: 約 25 KB