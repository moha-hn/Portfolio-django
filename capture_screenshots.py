"""Capture a single full-page screenshot per site, cropped to 1280x720."""
import os
from playwright.sync_api import sync_playwright

SITES = [
    {"slug": "boreal",    "url": "https://prod-production-8a67.up.railway.app/fr/"},
    {"slug": "ovalia",    "url": "https://bijouxovalia.com/"},
    {"slug": "margarita", "url": "https://placement-margarita.com/"},
]

MEDIA = os.path.join(os.path.dirname(__file__), "media")
W, H = 1280, 720

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": W, "height": H})
        page = ctx.new_page()
        for site in SITES:
            print(f"Shooting {site['slug']} …")
            try:
                page.goto(site["url"], wait_until="networkidle", timeout=30000)
            except Exception:
                page.goto(site["url"], wait_until="domcontentloaded", timeout=30000)
            page.keyboard.press("Escape")
            page.wait_for_timeout(1200)
            out = os.path.join(MEDIA, f"ss_{site['slug']}.jpg")
            page.screenshot(path=out, type="jpeg", quality=88, clip={"x":0,"y":0,"width":W,"height":H})
            kb = os.path.getsize(out) // 1024
            print(f"  ✓ {out}  ({kb} KB)")
        browser.close()

if __name__ == "__main__":
    main()
