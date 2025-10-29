# 📸 圖片資源總覽

所有圖片均為 SVG 向量圖形格式，可無限縮放且檔案小巧。

---

## 🎨 已生成的圖片清單

### 1. **品牌識別圖片**

#### [logo.svg](computer:///mnt/user-data/outputs/static/images/logo.svg) (1.2 KB)
**系統主 Logo - 藍色版本**
- 📐 尺寸: 200x200 px
- 🎨 配色: 藍色主題 (#0d6efd)
- 💡 設計: 錢包圖示 + 金錢符號 + 文字「財務管理」
- 📍 使用位置: 
  - 登入/註冊頁面
  - 關於頁面
  - 文件封面
- 使用範例:
  ```html
  <img src="{{ url_for('static', filename='images/logo.svg') }}" alt="財務管理系統" width="150">
  ```

#### [logo-white.svg](computer:///mnt/user-data/outputs/static/images/logo-white.svg) (1.2 KB)
**系統 Logo - 白色版本**
- 📐 尺寸: 200x200 px
- 🎨 配色: 白色主題（用於深色背景）
- 💡 設計: 與主 Logo 相同，顏色反轉
- 📍 使用位置: 
  - 深色主題導航欄
  - 深色背景區域
  - 列印友善版本
- 使用範例:
  ```html
  <img src="{{ url_for('static', filename='images/logo-white.svg') }}" alt="Logo" class="logo-dark-bg">
  ```

#### [favicon.svg](computer:///mnt/user-data/outputs/static/images/favicon.svg) (588 bytes)
**網站圖示（Favicon）**
- 📐 尺寸: 32x32 px
- 🎨 配色: 藍色背景 + 白色圖示
- 💡 設計: 簡化版錢包圖示
- 📍 使用位置: 
  - 瀏覽器標籤頁圖示
  - 書籤圖示
  - 捷徑圖示
- 使用範例:
  ```html
  <link rel="icon" type="image/svg+xml" href="{{ url_for('static', filename='images/favicon.svg') }}">
  ```

---

### 2. **功能圖示**

#### [icon-income.svg](computer:///mnt/user-data/outputs/static/images/icon-income.svg) (842 bytes)
**收入圖示**
- 📐 尺寸: 100x100 px
- 🎨 配色: 綠色 (#198754)
- 💡 設計: 向上箭頭 + 金錢符號
- 📍 使用位置: 
  - 儀表板收入卡片
  - 交易類型選擇
  - 統計圖表圖例

#### [icon-expense.svg](computer:///mnt/user-data/outputs/static/images/icon-expense.svg) (838 bytes)
**支出圖示**
- 📐 尺寸: 100x100 px
- 🎨 配色: 紅色 (#dc3545)
- 💡 設計: 向下箭頭 + 金錢符號
- 📍 使用位置: 
  - 儀表板支出卡片
  - 交易類型選擇
  - 統計圖表圖例

#### [icon-goal.svg](computer:///mnt/user-data/outputs/static/images/icon-goal.svg) (1.2 KB)
**目標圖示**
- 📐 尺寸: 100x100 px
- 🎨 配色: 青色 (#0dcaf0) + 黃色星星
- 💡 設計: 靶心 + 命中箭頭
- 📍 使用位置: 
  - 財務目標頁面
  - 目標卡片
  - 導航選單圖示

#### [icon-report.svg](computer:///mnt/user-data/outputs/static/images/icon-report.svg) (1.4 KB)
**報表圖示**
- 📐 尺寸: 100x100 px
- 🎨 配色: 紫色 (#6f42c1) + 黃色趨勢線
- 💡 設計: 文件 + 長條圖 + 趨勢線
- 📍 使用位置: 
  - 月報表頁面
  - 報表卡片
  - 導航選單圖示

---

### 3. **空狀態圖示**

#### [empty-state.svg](computer:///mnt/user-data/outputs/static/images/empty-state.svg) (1.2 KB)
**空狀態佔位圖**
- 📐 尺寸: 300x300 px
- 🎨 配色: 灰色系
- 💡 設計: 空資料夾 + 虛線文件
- 📍 使用位置: 
  - 無交易記錄時
  - 無目標時
  - 任何資料為空的情況
- 使用範例:
  ```html
  <div class="empty-state">
      <img src="{{ url_for('static', filename='images/empty-state.svg') }}" width="200">
      <p>暫無資料</p>
  </div>
  ```

#### [no-data.svg](computer:///mnt/user-data/outputs/static/images/no-data.svg) (1.6 KB)
**無資料圖示**
- 📐 尺寸: 300x300 px
- 🎨 配色: 灰色系
- 💡 設計: 剪貼板 + X 符號
- 📍 使用位置: 
  - 搜尋無結果
  - 篩選無資料
  - 報表無資料

#### [empty-chart.svg](computer:///mnt/user-data/outputs/static/images/empty-chart.svg) (2.7 KB)
**空白圖表圖示**
- 📐 尺寸: 300x300 px
- 🎨 配色: 灰色系
- 💡 設計: 座標軸 + 虛線長條 + 問號
- 📍 使用位置: 
  - 圖表無資料時
  - 統計資料不足
  - 載入圖表前的佔位

---

### 4. **錯誤頁面圖示**

#### [404.svg](computer:///mnt/user-data/outputs/static/images/404.svg) (1.4 KB)
**404 錯誤圖示**
- 📐 尺寸: 400x300 px
- 🎨 配色: 黃色 (#ffc107) + 紅色 X
- 💡 設計: 放大鏡 + X 符號 + 404 文字
- 📍 使用位置: 
  - 404 錯誤頁面
  - 找不到頁面時
- 使用範例:
  ```html
  <!-- templates/errors/404.html -->
  <img src="{{ url_for('static', filename='images/404.svg') }}" width="300">
  ```

#### [500.svg](computer:///mnt/user-data/outputs/static/images/500.svg) (1.8 KB)
**500 錯誤圖示**
- 📐 尺寸: 400x300 px
- 🎨 配色: 灰色伺服器 + 紅色/黃色指示燈
- 💡 設計: 伺服器機櫃 + 警告符號 + 閃電
- 📍 使用位置: 
  - 500 錯誤頁面
  - 伺服器錯誤時

---

### 5. **使用者相關**

#### [user-avatar-default.svg](computer:///mnt/user-data/outputs/static/images/user-avatar-default.svg) (509 bytes)
**預設使用者頭像**
- 📐 尺寸: 200x200 px
- 🎨 配色: 灰色系
- 💡 設計: 簡化人形輪廓
- 📍 使用位置: 
  - 使用者未上傳頭像時
  - 個人資料頁面
  - 導航欄使用者選單
- 使用範例:
  ```html
  <img src="{{ url_for('static', filename='images/user-avatar-default.svg') }}" 
       class="rounded-circle" width="40">
  ```

---

## 🎯 使用方式

### 在 HTML 模板中使用

```html
<!-- 方式 1: Flask url_for -->
<img src="{{ url_for('static', filename='images/logo.svg') }}" alt="Logo">

<!-- 方式 2: 直接路徑 -->
<img src="/static/images/icon-income.svg" alt="收入圖示">

<!-- 方式 3: 作為背景圖 -->
<div style="background-image: url('{{ url_for('static', filename='images/empty-state.svg') }}')"></div>
```

### 在 CSS 中使用

```css
.logo {
    background-image: url('../images/logo.svg');
    background-size: contain;
    background-repeat: no-repeat;
}

.empty-state::before {
    content: '';
    background: url('../images/no-data.svg') center/contain no-repeat;
}
```

### 在 JavaScript 中使用

```javascript
// 動態載入圖片
const img = document.createElement('img');
img.src = '/static/images/icon-goal.svg';
img.alt = '目標圖示';
document.body.appendChild(img);
```

---

## 📏 檔案規格

| 圖片 | 尺寸 | 檔案大小 | 用途 |
|------|------|----------|------|
| logo.svg | 200x200 | 1.2 KB | 品牌識別 |
| logo-white.svg | 200x200 | 1.2 KB | 深色背景 Logo |
| favicon.svg | 32x32 | 588 bytes | 網站圖示 |
| icon-income.svg | 100x100 | 842 bytes | 收入功能 |
| icon-expense.svg | 100x100 | 838 bytes | 支出功能 |
| icon-goal.svg | 100x100 | 1.2 KB | 目標功能 |
| icon-report.svg | 100x100 | 1.4 KB | 報表功能 |
| empty-state.svg | 300x300 | 1.2 KB | 空狀態 |
| no-data.svg | 300x300 | 1.6 KB | 無資料 |
| empty-chart.svg | 300x300 | 2.7 KB | 空圖表 |
| 404.svg | 400x300 | 1.4 KB | 404 錯誤 |
| 500.svg | 400x300 | 1.8 KB | 500 錯誤 |
| user-avatar-default.svg | 200x200 | 509 bytes | 預設頭像 |

**總計**: 13 個 SVG 檔案，約 **15 KB**

---

## ✨ SVG 格式優勢

### 為什麼選擇 SVG？

✅ **可無限縮放** - 不會失真或模糊  
✅ **檔案極小** - 平均每個檔案 < 2 KB  
✅ **CSS 可調** - 可用 CSS 改變顏色、大小  
✅ **動畫友善** - 支援 CSS/JS 動畫  
✅ **SEO 友善** - 搜尋引擎可讀取內容  
✅ **響應式** - 自動適應不同螢幕  

### 如何修改顏色？

```css
/* 方式 1: CSS filter */
.icon-income {
    filter: hue-rotate(90deg);
}

/* 方式 2: 直接修改 SVG fill 屬性 */
svg path {
    fill: #your-color;
}

/* 方式 3: 使用 CSS 變數 */
:root {
    --icon-color: #0d6efd;
}
```

---

## 🎨 配色方案

所有圖示遵循系統的配色方案：

| 類型 | 顏色 | 十六進位 | 用途 |
|------|------|----------|------|
| 主色 | 藍色 | #0d6efd | Logo、按鈕 |
| 成功/收入 | 綠色 | #198754 | 收入、成功訊息 |
| 危險/支出 | 紅色 | #dc3545 | 支出、錯誤 |
| 警告 | 黃色 | #ffc107 | 警告、提示 |
| 資訊 | 青色 | #0dcaf0 | 資訊、目標 |
| 次要 | 紫色 | #6f42c1 | 報表、次要功能 |
| 灰色系 | - | #6c757d | 空狀態、禁用 |

---

## 🔄 如何替換圖片

### 替換現有圖片

1. 準備新的 SVG 檔案
2. 確保檔名相同
3. 複製到 `static/images/` 資料夾
4. 清除瀏覽器快取

### 新增圖片

1. 設計新的 SVG 圖示
2. 優化 SVG 程式碼（移除不必要的標籤）
3. 放入 `static/images/` 資料夾
4. 在程式碼中引用

### 建議的 SVG 優化工具

- [SVGOMG](https://jakearchibald.github.io/svgomg/) - 線上 SVG 優化器
- [SVG Minifier](https://www.svgminify.com/) - SVG 壓縮工具

---

## 📱 響應式使用

### 不同螢幕尺寸的建議

```css
/* 手機 */
@media (max-width: 576px) {
    .logo { width: 100px; }
    .icon { width: 40px; }
}

/* 平板 */
@media (min-width: 577px) and (max-width: 991px) {
    .logo { width: 150px; }
    .icon { width: 60px; }
}

/* 桌面 */
@media (min-width: 992px) {
    .logo { width: 200px; }
    .icon { width: 80px; }
}
```

---

## 🚀 效能優化建議

### 1. 延遲載入
```html
<img src="{{ url_for('static', filename='images/logo.svg') }}" 
     loading="lazy" alt="Logo">
```

### 2. 使用 CSS Sprites
對於常用的小圖示，可以考慮合併成一個 SVG sprite

### 3. CDN 快取
如果部署到生產環境，建議使用 CDN 加速圖片載入

---

## 🎯 最佳實踐

### Do ✅
- 總是為圖片加上 `alt` 屬性
- 使用語義化的檔名
- 保持 SVG 程式碼簡潔
- 使用適當的尺寸

### Don't ❌
- 不要使用過大的 SVG
- 不要在 SVG 中嵌入點陣圖
- 不要忘記設定 viewport
- 不要使用絕對定位的 SVG

---

## 📞 需要更多圖片？

### 免費 SVG 資源網站

- [Heroicons](https://heroicons.com/)
- [Feather Icons](https://feathericons.com/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [Material Icons](https://fonts.google.com/icons)
- [Font Awesome](https://fontawesome.com/)
- [Flaticon](https://www.flaticon.com/)

---

**建立日期**: 2025 年 10 月 30 日  
**總圖片數**: 13 個 SVG 檔案  
**總檔案大小**: ~15 KB  
**格式**: SVG（可縮放向量圖形）