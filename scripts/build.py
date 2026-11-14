#!/usr/bin/env python3
"""
玻璃小店網站 — Build script
從 data/products.json (LINE Shop 產品) 生成靜態 HTML
"""
import json
import shutil
import urllib.parse
from pathlib import Path

SITE = Path(__file__).parent.parent
DATA = SITE / "data"
SRC = SITE / "src"
PUBLIC = SITE / "public"


def load_products():
    with open(DATA / "products.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_template(name):
    return (SRC / "templates" / name).read_text(encoding="utf-8")


def render_template(template_str, **kwargs):
    result = template_str
    for k, v in kwargs.items():
        result = result.replace("{{ " + k + " }}", str(v))
    return result


def build_index(products):
    """首頁"""
    shop = products["shop_name"]
    n = products["total_products"]
    
    # 分類（簡單規則）
    cards = []
    for p in products["products"][:8]:
        url_name = urllib.parse.quote(p["name"])
        cards.append(
            f'<a href="/products/{url_name}/" class="bottle-card">'
            f'<div class="bottle-name">{p["name"]}</div>'
            f'<div class="bottle-meta">{p["category"]}</div>'
            f'</a>'
        )
    
    template = load_template("index.html")
    html = render_template(
        template,
        SHOP_NAME=shop,
        TOTAL_PRODUCTS=n,
        TOP_PRODUCTS_HTML="\n".join(cards),
        SHOP_URL=products["shop_url"],
    )
    (PUBLIC / "index.html").write_text(html, encoding="utf-8")
    print(f"✓ index.html")


def build_products_index(products):
    """產品總覽頁"""
    # 分類
    categories = {}
    for p in products["products"]:
        cat = p.get("category", "其他")
        categories.setdefault(cat, []).append(p)
    
    cards = []
    for cat, items in sorted(categories.items()):
        cards.append(f'<h2 class="cat-title">{cat}（{len(items)} 款）</h2>')
        cards.append('<div class="bottles-grid">')
        for p in items:
            url_name = urllib.parse.quote(p["name"])
            cards.append(
                f'<a href="/products/{url_name}/" class="bottle-card">'
                f'<div class="bottle-name">{p["name"]}</div>'
                f'<div class="bottle-meta">{p.get("category", "")}</div>'
                f'</a>'
            )
        cards.append('</div>')
    
    template = load_template("products.html")
    html = render_template(template, PRODUCTS_HTML="\n".join(cards), TOTAL=len(products["products"]))
    (PUBLIC / "products").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "products" / "index.html").write_text(html, encoding="utf-8")
    print(f"✓ products/index.html")


def build_product_pages(products):
    """為每個 LINE Shop 產品生成獨立頁"""
    template = load_template("product.html")
    count = 0
    
    for p in products["products"]:
        name = p["name"]
        url_name = urllib.parse.quote(name)
        category = p.get("category", "其他")
        url = p["url"]
        
        # 簡易規格
        spec_html = ""
        if p.get("capacity"):
            spec_html += f'<li><strong>容量</strong>{p["capacity"]}</li>'
        if p.get("material"):
            spec_html += f'<li><strong>材質</strong>{p["material"]}</li>'
        if p.get("usage"):
            spec_html += f'<li><strong>適用</strong>{p["usage"]}</li>'
        if not spec_html:
            spec_html = '<li>完整規格請見 LINE Shop 商品頁</li>'
        
        # CTA：直接到 LINE Shop
        cta_html = (
            f'<a href="{url}" class="btn-primary" target="_blank" rel="noopener">'
            f'前往 LINE Shop 購買 →</a>'
            f'<p class="cta-hint">在 {products["shop_name"]} 完成下單、付款、出貨</p>'
        )
        
        # 用途（從分類推論）
        category = p.get("category", "")
        if "梅酒" in category or "酒" in name:
            uses = '<li>梅酒、其他水果酒</li><li>浸泡醋</li><li>自製藥酒</li>'
        elif "醬菜" in category or "果醬" in category:
            uses = '<li>糖漬柚皮、果醬</li><li>手工味噌、豆腐乳</li><li>XO 醬</li>'
        elif "油品" in category or "油" in name:
            uses = '<li>橄欖油、苦茶油</li><li>精油（按摩、香氛）</li><li>醬油、醋</li>'
        elif "蜂蜜" in category:
            uses = '<li>蜂蜜、楓糖漿</li><li>柚子茶（沖泡用）</li>'
        else:
            uses = '<li>各式手工食品保存</li><li>禮品包裝</li>'
        
        html = render_template(
        template,
            PRODUCT_NAME=name,
            CATEGORY=category,
            SPEC_HTML=spec_html,
            USES_HTML=uses,
            CTA_HTML=cta_html,
            META_DESC=f"{name} — {category}，玻璃小店 {products['shop_name']} 提供。",
            OG_TITLE=f"{name} — 玻璃小店",
            OG_DESC=f"{category}，玻璃小店 LINE Shop 提供。",
            OG_URL=f"/products/{url_name}/",
        )
        
        # 寫入 /products/{name}/index.html
        product_dir = PUBLIC / "products" / name
        product_dir.mkdir(parents=True, exist_ok=True)
        (product_dir / "index.html").write_text(html, encoding="utf-8")
        count += 1
    
    print(f"✓ 為 {count} 個 LINE Shop 產品生成了獨立頁")


def copy_assets():
    assets_src = SRC / "assets"
    assets_dst = PUBLIC / "assets"
    assets_dst.mkdir(parents=True, exist_ok=True)
    for f in assets_src.iterdir():
        if f.is_file():
            shutil.copy(f, assets_dst / f.name)
    print(f"✓ assets/")


def main():
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "assets").mkdir(parents=True, exist_ok=True)
    
    products = load_products()
    print(f"資料來源：LINE Shop {products['shop_name']}，{products['total_products']} 個產品\n")
    
    build_index(products)
    build_products_index(products)
    build_product_pages(products)
    copy_assets()
    
    print(f"\nBuild 完成！輸出在 {PUBLIC}/")


if __name__ == "__main__":
    main()
