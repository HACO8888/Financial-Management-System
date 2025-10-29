# 🚀 快速啟動指南

這份指南將幫助你在 5 分鐘內啟動財務管理系統！

---

## ⚡ 一鍵啟動（適合急著使用的人）

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 初始化資料庫
python init_db.py

# 3. 啟動應用程式
python app.py
```

然後開啟瀏覽器前往 `http://localhost:5000`

**測試帳號**: test / test123

---

## 📋 詳細步驟

### 步驟 1: 準備環境

確保你已安裝：
- ✅ Python 3.8 或更高版本
- ✅ pip（Python 套件管理器）

檢查版本：
```bash
python --version
pip --version
```

### 步驟 2: 下載專案

將所有檔案放到一個資料夾中，例如 `finance_manager/`

確保資料夾結構如下：
```
finance_manager/
├── app.py
├── config.py
├── models.py
├── init_db.py
├── requirements.txt
├── routes/
├── services/
├── utils/
├── templates/
└── static/
```

### 步驟 3: 建立虛擬環境（建議）

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 步驟 4: 安裝依賴套件

```bash
pip install -r requirements.txt
```

這會安裝：
- Flask (Web 框架)
- SQLAlchemy (ORM)
- PostgreSQL 驅動
- Flask-Login (使用者驗證)
- APScheduler (排程任務)
- 其他必要套件

### 步驟 5: 初始化資料庫

```bash
python init_db.py
```

你會看到：
```
🗄️  開始初始化資料庫...
✅ 資料表建立完成
✅ 測試使用者建立完成 (帳號: test, 密碼: test123)
✅ 預設類別建立完成
🎉 資料庫初始化完成！
```

### 步驟 6: 啟動應用程式

```bash
python app.py
```

你會看到：
```
🚀 財務管理系統啟動中...
📊 環境: development
🌐 訪問網址: http://localhost:5000
 * Running on http://0.0.0.0:5000
```

### 步驟 7: 開始使用

1. 開啟瀏覽器
2. 前往 `http://localhost:5000`
3. 使用測試帳號登入：
   - 帳號：`test`
   - 密碼：`test123`

---

## 🎯 首次使用建議

登入後，按照以下順序體驗系統：

### 1. 查看儀表板
- 了解系統整體佈局
- 查看統計卡片

### 2. 新增交易記錄
1. 點擊「交易管理」
2. 點擊「新增交易」
3. 選擇類型（收入或支出）
4. 選擇類別
5. 輸入金額和日期
6. 儲存

### 3. 設定財務目標
1. 點擊「財務目標」
2. 點擊「新增目標」
3. 輸入目標名稱（例如：存錢買筆電）
4. 選擇目標類型（儲蓄或支出限制）
5. 設定目標金額
6. 選擇期限
7. 建立

### 4. 查看報表
1. 點擊「月報表」
2. 選擇「生成報表」
3. 選擇年份和月份
4. 查看詳細分析

### 5. 管理類別
1. 點擊右上角使用者選單
2. 選擇「類別管理」
3. 新增自訂收入或支出類別

---

## 🔧 常見問題解決

### 問題 1: 無法連接資料庫

**錯誤訊息**: `could not connect to server`

**解決方法**:
- 確認 PostgreSQL 連接字串正確
- 檢查網路連接
- 確認 Zeabur 資料庫服務正常運行

### 問題 2: 模組未找到

**錯誤訊息**: `ModuleNotFoundError: No module named 'flask'`

**解決方法**:
```bash
pip install -r requirements.txt
```

### 問題 3: 端口已被佔用

**錯誤訊息**: `Address already in use`

**解決方法**:
1. 關閉佔用 5000 端口的程式
2. 或修改 `app.py` 中的端口號

### 問題 4: 無法建立資料表

**錯誤訊息**: `permission denied`

**解決方法**:
- 確認資料庫使用者有建立表的權限
- 檢查資料庫連接字串中的使用者名稱和密碼

---

## 🎨 自訂設定

### 修改端口號

編輯 `app.py`：
```python
app.run(host='0.0.0.0', port=8080, debug=debug_mode)
```

### 修改密鑰

建立 `.env` 檔案：
```
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### 修改資料庫連接

編輯 `config.py`：
```python
SQLALCHEMY_DATABASE_URI = 'your-database-url'
```

---

## 📊 功能測試清單

完成這些步驟以確保系統正常運作：

- [ ] ✅ 註冊新帳號
- [ ] ✅ 登入系統
- [ ] ✅ 新增一筆收入記錄
- [ ] ✅ 新增一筆支出記錄
- [ ] ✅ 編輯交易記錄
- [ ] ✅ 刪除交易記錄
- [ ] ✅ 新增自訂類別
- [ ] ✅ 設定一個財務目標
- [ ] ✅ 查看目標進度
- [ ] ✅ 生成月報表
- [ ] ✅ 查看報表詳情
- [ ] ✅ 查看圖表視覺化
- [ ] ✅ 登出系統

---

## 🔄 停止應用程式

在終端機中按 `Ctrl + C`

---

## 📱 行動裝置使用

系統支援響應式設計，你可以：

1. 在手機瀏覽器輸入電腦的 IP 位址和端口
   例如：`http://192.168.1.100:5000`

2. 或使用 ngrok 建立公開網址：
```bash
# 安裝 ngrok
# 執行
ngrok http 5000
```

---

## 🎓 下一步學習

完成基本操作後，你可以：

1. **探索進階功能**
   - 查看分析見解
   - 閱讀理財建議
   - 比較不同月份報表

2. **自訂系統**
   - 修改 CSS 樣式
   - 新增自己的類別
   - 調整統計方式

3. **部署到線上**
   - 參考 README.md 的部署指南
   - 使用 Heroku、Railway 或 Render

---

## 💡 提示與技巧

### 提示 1: 快速新增記錄
直接點擊儀表板上的「新增交易」按鈕

### 提示 2: 批次匯入
如果有大量歷史資料，可以直接操作資料庫匯入

### 提示 3: 備份資料
定期備份 PostgreSQL 資料庫

### 提示 4: 查看日誌
在終端機中查看即時日誌，幫助除錯

### 提示 5: 離線使用
系統設計為 Web 應用，需要網路連接到資料庫

---

## 🆘 需要幫助？

- 📖 閱讀 [README.md](computer:///mnt/user-data/outputs/README.md) 完整說明
- 📝 查看專案內的程式碼註解
- 🔍 搜尋 Flask 或 SQLAlchemy 官方文件

---

**祝你使用愉快！開始管理你的財務吧！** 💰📊📈

---

**最後更新**: 2025 年 10 月 30 日