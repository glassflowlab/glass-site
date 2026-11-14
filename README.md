# 玻璃小店網站

> 殼網站 + LINE Shop 成交架構
> 內容在自己網域、未來不被 LINE 鎖住。

## 架構

    [FB / IG / SEO / Google]
            ↓
       玻璃小店網站（本專案）
       - 每月一物
       - 瓶款介紹（121 種）
       - 食譜/客戶故事
            ↓ 點前往 LINE Shop
       LINE Shop 成交
       - oashop.line.me/@lrg1884b
       - 5,212 好友

## 分離架構

| 系統 | 位置 | 部署 |
|---|---|---|
| 客戶尋回（內部） | ~/玻璃小店/客戶系統/ | 本地 Flask |
| 部落格素材 | ~/玻璃小店/blog/ | 本地 HTTP |
| 殼網站 | ~/玻璃小店/site/ | Cloudflare Pages |

## 專案結構

    site/
    ├── public/             Build 產出（部署用）
    ├── src/
    │   ├── templates/      HTML 模板
    │   └── assets/         CSS
    ├── scripts/
    │   └── build.py        Build script
    ├── data-public/        公開資料快照
    │   ├── bottles.json    121 種瓶款（不含個資）
    │   ├── summary.json    客戶總數、年度彙總
    │   └── lineshop.json   LINE Shop 商品
    └── content/            內容源（每月一物、食譜）

## 公開資料怎麼來的

    customers.db（本地）
       ↓ extract_public.py（本地執行）
    data-public/bottles.json    只含瓶款名、客戶數、交易次數
                              （沒有姓名、電話、地址、對話）

    customers.db 不會上傳到雲端。

## 開發流程

### 重新整理公開資料

    cd ~/Documents/玻璃小店/site
    python3 scripts/extract_public.py

### Build

    cd ~/Documents/玻璃小店/site
    python3 scripts/build.py

### 本地預覽

    cd ~/Documents/玻璃小店/site/public
    python3 -m http.server 8081

## 資料現況（2026-09-02）

- 客戶總數：29,715（彙總）
- 瓶款：121 種
- 年度銷售：2022-2026 共 5 年
- LINE Shop 商品：20 個（首頁熱門區）

## TODO

- [ ] 註冊網域（WantEasy，NT$349/年）
- [ ] 連接 Cloudflare Pages
- [ ] 每月一物頁版型
- [ ] 食譜頁版型
- [ ] 單一產品頁（含 LINE Shop 連結）
- [ ] 單一月度頁（SEO 友善 URL）
- [ ] sitemap.xml
- [ ] Google Search Console
- [ ] GA4
- [ ] 從 LINE Shop 自動同步價格