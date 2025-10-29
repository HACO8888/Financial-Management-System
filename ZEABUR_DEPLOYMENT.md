# 🚀 Zeabur 部署指南

## 📋 問題診斷與修復

### 問題：`Failed to find attribute 'app' in 'app'`

**原因**：gunicorn 找不到 Flask 應用實例

**已修復**：`app.py` 已更新，現在在模組層級創建 `app` 實例

---

## ✅ 修復後的 app.py 結構

```python
def create_app(config_name='development'):
    # ... 創建和配置 Flask 應用
    return app

# ⭐ 重要：為 gunicorn 創建應用實例
app = create_app(os.environ.get('FLASK_ENV', 'production'))

if __name__ == '__main__':
    # 開發模式
    dev_app = create_app('development')
    dev_app.run(...)
```

---

## 🔧 Zeabur 部署步驟

### 步驟 1: 準備檔案

確保你的專案包含以下檔案：

```
finance_manager/
├── app.py                 # ✅ 已修復
├── requirements.txt       # Python 依賴
├── models.py             # 資料模型
├── config.py             # 配置
├── routes/               # 路由
├── services/             # 服務
├── templates/            # 模板
├── static/               # 靜態資源
└── utils/                # 工具
```

### 步驟 2: 推送代碼到 Git

```bash
git init
git add .
git commit -m "Deploy to Zeabur"
git remote add origin YOUR_GIT_URL
git push -u origin main
```

### 步驟 3: 在 Zeabur 創建服務

1. 登入 [Zeabur Dashboard](https://dash.zeabur.com)
2. 點擊「Create Project」
3. 選擇你的 Git 倉庫
4. Zeabur 會自動檢測為 Python 專案

### 步驟 4: 配置環境變數

在 Zeabur 控制台設定以下環境變數：

#### 必需的環境變數

| 變數名 | 值 | 說明 |
|--------|-----|------|
| `FLASK_ENV` | `production` | 生產環境 |
| `SECRET_KEY` | `your-random-secret-key` | Flask 密鑰（必須隨機生成） |
| `DATABASE_URL` | `postgresql://...` | PostgreSQL 連接字串 |

#### 可選的環境變數

| 變數名 | 值 | 說明 |
|--------|-----|------|
| `PORT` | `8080` | 端口號（Zeabur 自動設定） |
| `ENABLE_SCHEDULER` | `true` | 啟用自動排程（月報表） |
| `INIT_DB` | `true` | 首次部署時初始化資料庫 |

### 步驟 5: 設定啟動命令

Zeabur 通常會自動檢測，但如果需要手動設定：

**啟動命令**：
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

或在專案根目錄創建 `Procfile`：
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
```

### 步驟 6: 初始化資料庫

首次部署後，需要初始化資料庫：

**方法 1：使用環境變數**
1. 設定 `INIT_DB=true`
2. 重新部署
3. 部署成功後移除 `INIT_DB` 變數

**方法 2：使用 Zeabur 終端**
1. 在 Zeabur 控制台打開終端
2. 執行：
```bash
python init_db.py
```

**方法 3：本地連接資料庫**
```bash
# 使用 Zeabur 提供的 DATABASE_URL
export DATABASE_URL="postgresql://..."
python init_db.py
```

### 步驟 7: 驗證部署

1. 訪問 Zeabur 提供的 URL
2. 應該看到登入頁面
3. 使用測試帳號登入：
   - 帳號：`test`
   - 密碼：`test123`

---

## 🔐 生成 SECRET_KEY

在 Python 中生成隨機密鑰：

```python
import secrets
print(secrets.token_hex(32))
```

或使用命令行：
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🗄️ PostgreSQL 資料庫配置

### 使用 Zeabur PostgreSQL

1. 在 Zeabur 專案中添加 PostgreSQL 服務
2. Zeabur 會自動設定 `DATABASE_URL` 環境變數
3. 不需要手動配置連接字串

### 資料庫連接字串格式

```
postgresql://username:password@host:port/database
```

例如：
```
postgresql://user:pass@db.zeabur.com:5432/finance_db
```

---

## 🐛 常見問題排查

### 問題 1: 應用無法啟動

**錯誤**: `Failed to find attribute 'app' in 'app'`

**解決**:
- 確認使用最新的 `app.py`（已包含模組層級的 app 實例）
- 檢查啟動命令是否為 `gunicorn app:app`

### 問題 2: 資料庫連接失敗

**錯誤**: `could not connect to server`

**解決**:
- 檢查 `DATABASE_URL` 環境變數是否正確
- 確認 PostgreSQL 服務正在運行
- 檢查網路連接

### 問題 3: 靜態文件無法載入

**解決**:
- Zeabur 會自動處理靜態文件
- 確認 `static/` 資料夾在專案根目錄
- 檢查 Flask 配置中的 `STATIC_FOLDER` 設定

### 問題 4: 模組導入錯誤

**錯誤**: `ModuleNotFoundError: No module named 'xxx'`

**解決**:
- 檢查 `requirements.txt` 是否包含所有依賴
- 確認依賴版本相容
- 查看 Zeabur 構建日誌

---

## 📊 監控與日誌

### 查看日誌

1. 進入 Zeabur 控制台
2. 選擇你的服務
3. 點擊「Logs」標籤
4. 查看即時日誌

### 重要日誌訊息

**成功啟動**:
```
[INFO] Starting gunicorn
[INFO] Listening at: http://0.0.0.0:8080
[INFO] Booting worker with pid: X
✅ 資料表已建立
```

**錯誤訊息**:
```
[ERROR] Worker exited with code 4
[ERROR] App failed to load
```

---

## 🔄 更新部署

### 推送更新

```bash
git add .
git commit -m "Update application"
git push origin main
```

Zeabur 會自動檢測更改並重新部署。

### 手動觸發部署

在 Zeabur 控制台點擊「Redeploy」按鈕。

---

## ⚙️ 性能優化

### Worker 數量

根據 CPU 核心數調整：
```bash
gunicorn app:app --workers $(( 2 * $(nproc) + 1 ))
```

或固定數量：
```bash
gunicorn app:app --workers 4
```

### 超時設定

對於較慢的操作（如報表生成）：
```bash
gunicorn app:app --timeout 300
```

### 日誌級別

生產環境建議：
```bash
gunicorn app:app --log-level warning
```

---

## 🔒 安全建議

### 1. 使用強密碼

- `SECRET_KEY` 必須是隨機生成的長字串
- 資料庫密碼應該足夠複雜

### 2. HTTPS

Zeabur 自動提供 HTTPS，無需額外配置。

### 3. 環境變數

- 不要在代碼中硬編碼密碼
- 使用 Zeabur 環境變數功能

### 4. 資料庫備份

定期備份 PostgreSQL 資料庫：
```bash
pg_dump $DATABASE_URL > backup.sql
```

---

## 📈 擴展建議

### 添加自訂域名

1. 在 Zeabur 控制台添加域名
2. 配置 DNS 記錄
3. Zeabur 自動配置 SSL

### 啟用 CDN

對於靜態資源，考慮使用 CDN 加速。

### 資料庫索引

在生產環境添加索引以提升性能：
```sql
CREATE INDEX idx_transactions_user_date ON transactions(user_id, date);
CREATE INDEX idx_goals_user_status ON goals(user_id, status);
```

---

## 🎯 部署檢查清單

部署前確認：

- [ ] `app.py` 已更新（包含模組層級的 app 實例）
- [ ] `requirements.txt` 包含所有依賴
- [ ] 環境變數已設定（SECRET_KEY, DATABASE_URL）
- [ ] PostgreSQL 服務已啟動
- [ ] 資料庫已初始化
- [ ] 測試帳號可以登入
- [ ] 靜態文件正確載入
- [ ] 所有路由正常運作

---

## 📞 需要幫助？

### Zeabur 文件

- [Zeabur 官方文件](https://zeabur.com/docs)
- [Python 部署指南](https://zeabur.com/docs/deploy/python)

### 專案文件

- [README.md](./README.md) - 專案說明
- [QUICK_START.md](./QUICK_START.md) - 快速開始

---

## ✅ 部署完成！

如果一切順利，你現在應該能夠：

1. ✅ 訪問 Zeabur 提供的 URL
2. ✅ 看到登入頁面
3. ✅ 成功登入系統
4. ✅ 使用所有功能
5. ✅ 自動生成月報表（如果啟用排程器）

**恭喜！你的財務管理系統已成功部署到 Zeabur！** 🎉

---

**更新日期**: 2025 年 10 月 30 日  
**版本**: 1.0.0  
**狀態**: ✅ 已修復部署問題