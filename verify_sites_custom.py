from playwright.sync_api import sync_playwright
import os

def verify_sites():
    sites = [
        ("neumann", "Dachdecker Neumann - Ihr Traditionsbetrieb in Frankfurt", "De-Neufville-Str. 27, 60596 Frankfurt am Main"),
        ("voelker", "Völkerdach - Qualität seit Generationen", "Oberschelder Weg 20, 60439 Frankfurt am Main")
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for folder, title_text, address in sites:
            path = os.path.abspath(f"kunden_websites/{folder}/index.html")
            print(f"Verifying {folder}...")
            page.goto(f"file://{path}")

            # Verify Title
            page_title = page.title()
            if title_text not in page_title:
                print(f"FAILED: Title mismatch for {folder}. Expected '{title_text}', got '{page_title}'")
            else:
                print(f"PASSED: Title verified for {folder}")

            # Verify Address in Footer
            content = page.content()
            if address in content:
                print(f"PASSED: Address verified for {folder}")
            else:
                print(f"FAILED: Address mismatch for {folder}. Expected '{address}'")

            # Verify Bugfixes
            # 1. Benefits Section bg-gray-100
            # We can check class existence
            benefits_section = page.locator("section.bg-gray-100").first
            if benefits_section.is_visible():
                print(f"PASSED: Benefits section has bg-gray-100 for {folder}")
            else:
                 print(f"FAILED: Benefits section missing bg-gray-100 for {folder}")

            # Screenshot
            page.screenshot(path=f"verification_{folder}.png")
            print(f"Screenshot saved to verification_{folder}.png")

        browser.close()

if __name__ == "__main__":
    verify_sites()
