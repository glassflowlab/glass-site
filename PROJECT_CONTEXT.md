# 玻璃小店網站專案 — 上下文（給未來的對話讀）

> 如果你（AI agent）剛被開到這個對話，請先讀這個檔案！
> 這會讓你知道：專案是什麼、為什麼這樣做、目前進度、下一步。

---

## 這是什麼

玻璃小店（LINE 開店 ID: @lrg1884b）的對外殼網站。

**架構（極簡）：**

- **這個專案（網站）** → ~/Documents/玻璃小店/site/ ← 你在這裡
- 客戶尋回系統 → ~/glassshop_system/ ← **獨立運作，不在本專案**
- LINE Shop 成交 → https://oashop.line.me/shops/@lrg1884b

**資料源（極簡）：**

- 只有一個：LINE Shop 商品（透過本專案手動下載或同步）
- 沒有 customers.db、沒有 LINE 對話、沒有其他來源

**商業邏輯：**

1. 用戶（FB、IG、Google）進到網站
2. 看瓶款
3. 點「前往 LINE Shop」→ 跳到 LINE Shop 下單
4. LINE Shop 用 LINE Pay 收款

---

## 為什麼這個架構（乾淨的設計決策）

- **只有一個資料源**（LINE Shop）：容易維護、不依賴內部資料庫
- **殼網站不下單、不收個資**：客戶資料留在 LINE
- **資料可以更新**：未來可以從 LINE Shop 商家後台下載 CSV 取代

---

## 已完成（截至 2026-09-02）

1. **極簡專案結構**
   - data/products.json ← LINE Shop 20 個商品
   - scripts/build.py ← 從 products.json 生成靜態網站
   - src/templates/ ← 3 個 HTML 模板
   - public/ ← build 產出（部署用）

2. **網站功能**
   - 首頁（推薦 + LINE Shop 按鈕）
   - 所有瓶款總覽（按分類）
   - 每個 LINE Shop 產品的獨立頁（直接到 LINE Shop 下單）

3. **本地預覽 server**（launchd）
   - port 8081
   - http://localhost:8081/
   - Tailscale：http://100.94.94.26:8081/

---

## 檔案結構

```
site/
├── README.md
├── PROJECT_CONTEXT.md          ← 你正在看
├── data/
│   └── products.json           ← LINE Shop 產品（唯一資料源）
├── scripts/
│   └── build.py                ← 生成靜態網站
├── src/
│   ├── templates/
│   │   ├── index.html
│   │   ├── products.html
│   │   └── product.html
│   └── assets/style.css
└── public/                     ← build 產出
    ├── index.html
    ├── products/index.html
    ├── products/{20 個}/index.html
    └── assets/style.css
```

---

## 開發指令

### 重新整理產品資料（從 LINE Shop）

未來可以從 LINE Shop 商家後台下載 CSV，把 products.json 替換掉：

1. 登入 https://oashop.line.me （商家管理）
2. 商品管理 → 匯出商品（CSV 格式）
3. 存到 `site/data/products.csv`
4. 改 build.py 從 CSV 讀（目前從 JSON 讀）

### Build 靜態網站

```bash
cd ~/Documents/玻璃小店/site
python3 scripts/build.py
```

### 本地預覽

http://localhost:8081/

### 重啟 server（如果掛了）

```bash
launchctl unload ~/Library/LaunchAgents/com.glassshop.site.plist
launchctl load ~/Library/LaunchAgents/com.glassshop.site.plist
```

---

## 下一步（優先順序）

### P1：實際 LINE Shop 產品 CSV

- [ ] 從 LINE Shop 商家後台下載真實商品 CSV
- [ ] 改 build.py 從 CSV 讀
- [ ] 確認 20 個商品（或其他數量）都正確

### P1：SEO

- [ ] sitemap.xml（自動生成）
- [ ] robots.txt
- [ ] Schema.org 結構化資料

### P2：正式部署

- [ ] 申請網域（WantEasy，NT$349/年）
- [ ] 連接 GitHub
- [ ] Cloudflare Pages 部署

### P3：未來可做

- [ ] 每月一物內容（從 blog 搬過來）
- [ ] GA4
- [ ] Google Search Console

---

## 關於用戶

- 玻璃小店老闆
- 用戶很懂自己的事業、客戶、市場
- 不一定懂技術（我說的話要白話一點）
- 喜歡「乾淨」的架構

---

## 如果遇到問題

1. 看 README.md（架構、開發流程）
3. 看 scripts/build.py（程式碼）
4. 如果還是不懂 — 問用戶，他會解釋背景
