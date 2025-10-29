# 📁 Images 資料夾

此資料夾用於存放系統使用的圖片資源。

## 建議的圖片檔案

### 1. **Logo 圖片**
- `logo.png` - 系統 Logo（建議尺寸：200x200 px）
- `logo-white.png` - 白色版本 Logo（用於深色背景）
- `favicon.ico` - 網站圖示（16x16, 32x32, 48x48 px）

### 2. **佔位圖片**
- `no-data.svg` - 無資料佔位圖
- `empty-chart.svg` - 空白圖表佔位圖
- `user-avatar-default.png` - 預設使用者頭像

### 3. **背景圖片**
- `login-bg.jpg` - 登入頁面背景（選用）
- `dashboard-bg.svg` - 儀表板背景圖案（選用）

### 4. **圖示**
- `icon-income.svg` - 收入圖示
- `icon-expense.svg` - 支出圖示
- `icon-goal.svg` - 目標圖示
- `icon-report.svg` - 報表圖示

## 使用方式

在 HTML 中引用圖片：
```html
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```

在 CSS 中引用圖片：
```css
background-image: url('../images/login-bg.jpg');
```

## 圖片優化建議

1. **格式選擇**
   - Logo/圖示：使用 SVG 格式（可縮放、檔案小）
   - 照片：使用 JPG 格式（壓縮率高）
   - 透明背景：使用 PNG 格式

2. **檔案大小**
   - 單個圖片建議不超過 500 KB
   - 使用線上工具壓縮圖片（如 TinyPNG）

3. **命名規範**
   - 使用小寫英文字母
   - 單字間用連字號（-）分隔
   - 有意義的檔名（如 `user-avatar-default.png`）

## 線上圖片資源

如果需要免費圖片，可以使用：
- [Unsplash](https://unsplash.com/) - 免費高品質照片
- [Pexels](https://www.pexels.com/) - 免費圖片和影片
- [Flaticon](https://www.flaticon.com/) - 免費圖示
- [Heroicons](https://heroicons.com/) - 免費 SVG 圖示
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Bootstrap 圖示庫

## 當前使用的圖示

目前系統使用 **Bootstrap Icons**，透過 CDN 載入，無需下載圖片檔案。

如果需要離線使用，可以下載 Bootstrap Icons 字型檔案放在此資料夾。

---

**注意**: 請確保使用的圖片有適當的授權，避免侵權問題。