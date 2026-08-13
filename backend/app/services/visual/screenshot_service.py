from pathlib import Path
from playwright.sync_api import sync_playwright
import time


UPLOAD_DIR = Path("backend/uploads/visual")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def capture_screenshot(url: str):

    filename = f"{int(time.time())}.png"

    save_path = UPLOAD_DIR / filename

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1440,
                "height": 1200
            }
        )

        page.goto(
            url,
            wait_until="networkidle",
            timeout=30000
        )

        page.screenshot(
            path=str(save_path),
            full_page=True
        )

        browser.close()

    return str(save_path)