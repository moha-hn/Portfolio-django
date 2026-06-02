"""
Capture scrolling GIFs of live project sites using Playwright + ffmpeg.
Output: media/gif_boreal.gif, media/gif_ovalia.gif, media/gif_margarita.gif
"""
import os, subprocess, shutil, tempfile
from playwright.sync_api import sync_playwright

SITES = [
    {
        "slug": "boreal",
        "url": "https://prod-production-8a67.up.railway.app/fr/",
        "scroll_to": 1800,
    },
    {
        "slug": "ovalia",
        "url": "https://bijouxovalia.com/",
        "scroll_to": 1800,
    },
    {
        "slug": "margarita",
        "url": "https://placement-margarita.com/",
        "scroll_to": 1800,
    },
]

WIDTH, HEIGHT = 1280, 720
FRAMES_PER_SITE = 40   # screenshots per site
GIF_FPS = 12
MEDIA_DIR = os.path.join(os.path.dirname(__file__), "media")


def capture_site(page, slug, url, scroll_to):
    tmpdir = tempfile.mkdtemp(prefix=f"gif_{slug}_")
    print(f"  → {url}")
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
    except Exception:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)

    # close cookie banners / popups by pressing Escape
    page.keyboard.press("Escape")
    page.wait_for_timeout(800)

    step = scroll_to / FRAMES_PER_SITE
    for i in range(FRAMES_PER_SITE):
        page.evaluate(f"window.scrollTo(0, {int(step * i)})")
        page.wait_for_timeout(60)
        page.screenshot(path=os.path.join(tmpdir, f"frame_{i:03d}.png"))

    # scroll back to top and grab a few more frames (nice loop)
    for i in range(5):
        page.evaluate(f"window.scrollTo(0, {max(0, scroll_to - int(step * i * 2))})")
        page.wait_for_timeout(60)
        page.screenshot(path=os.path.join(tmpdir, f"frame_r{i:03d}.png"))

    out_gif = os.path.join(MEDIA_DIR, f"gif_{slug}.gif")

    # use ffmpeg: png frames → palette → gif
    frames_glob = os.path.join(tmpdir, "frame*.png")
    palette = os.path.join(tmpdir, "_palette.png")
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(GIF_FPS),
        "-pattern_type", "glob",
        "-i", frames_glob,
        "-vf", f"scale={WIDTH}:{HEIGHT}:flags=lanczos,palettegen",
        palette,
    ], check=True, capture_output=True)

    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(GIF_FPS),
        "-pattern_type", "glob",
        "-i", frames_glob,
        "-i", palette,
        "-lavfi", f"scale={WIDTH}:{HEIGHT}:flags=lanczos[x];[x][1:v]paletteuse",
        out_gif,
    ], check=True, capture_output=True)

    shutil.rmtree(tmpdir)
    size_kb = os.path.getsize(out_gif) // 1024
    print(f"  ✓ {out_gif}  ({size_kb} KB)")
    return out_gif


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT})
        page = ctx.new_page()
        # hide cookie banners generically
        page.add_init_script("""
            document.addEventListener('DOMContentLoaded', () => {
                const sel = '[class*=cookie],[id*=cookie],[class*=gdpr],[id*=gdpr],[class*=consent],[id*=consent]';
                document.querySelectorAll(sel).forEach(el => el.remove());
            });
        """)
        for site in SITES:
            print(f"Capturing {site['slug']} ...")
            capture_site(page, site["slug"], site["url"], site["scroll_to"])
        browser.close()
    print("\nAll done.")


if __name__ == "__main__":
    main()
