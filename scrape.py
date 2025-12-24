import json, re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE = "https://www.steamartworkdesigns.com"
SHOP = BASE + "/shop"
MAX_PAGES = 12  # o /shop tem paginação (1..12)

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (catalog-gif-bot/1.0)"
})

# GIFs no Wix: static.wixstatic.com/media/...gif...
GIF_RE = re.compile(r"https?://static\.wixstatic\.com/media/[^\s\"')]+?\.gif[^\s\"')]*", re.I)

def fetch(url: str) -> str:
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r.text

def product_links(shop_html: str):
    soup = BeautifulSoup(shop_html, "html.parser")
    links = set()
    for a in soup.select("a[href]"):
        href = a.get("href", "")
        if "/product-page/" in href:
            links.add(urljoin(BASE, href))
    return links

def extract_title(soup: BeautifulSoup, fallback: str):
    h1 = soup.find("h1")
    if h1:
        t = h1.get_text(strip=True)
        if t:
            return t
    return fallback

def main():
    products = set()

    # varre /shop?page=N
    for p in range(1, MAX_PAGES + 1):
        url = SHOP if p == 1 else f"{SHOP}?page={p}"
        try:
            html = fetch(url)
            products |= product_links(html)
        except Exception:
            continue

    items = []
    seen = set()

    for u in sorted(products):
        try:
            html = fetch(u)
            soup = BeautifulSoup(html, "html.parser")
            title = extract_title(soup, u.split("/")[-1])

            gifs = GIF_RE.findall(html)
            for g in gifs:
                if g in seen:
                    continue
                seen.add(g)
                items.append({
                    "title": title,
                    "gif": g,
                    "source": u,
                    "category": None
                })
        except Exception:
            continue

    with open("gifs.json", "w", encoding="utf-8") as f:
        json.dump({"items": items, "source": SHOP}, f, ensure_ascii=False, indent=2)

    print(f"OK: {len(items)} gifs")

if __name__ == "__main__":
    main()
