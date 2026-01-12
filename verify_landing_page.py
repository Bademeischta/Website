
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the local file
        file_path = os.path.abspath("index.html")
        page.goto(f"file://{file_path}")

        # Wait for content to load and animations (if any)
        page.wait_for_timeout(1000)

        # Take a full page screenshot
        screenshot_path = "/home/jules/verification/landing_page.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    run()
