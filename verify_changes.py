from playwright.sync_api import sync_playwright

def verify_changes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Desktop context
        context_desktop = browser.new_context(viewport={'width': 1280, 'height': 800})
        page_desktop = context_desktop.new_page()
        page_desktop.goto("http://localhost:8000/index.html")

        # Verify Footer Address
        print("Verifying Footer Address...")
        footer = page_desktop.locator("footer")
        footer.scroll_into_view_if_needed()
        expect_address = footer.get_by_text("Dachstraße 1, 12345 Musterstadt")
        if expect_address.is_visible():
            print("SUCCESS: Address found in footer.")
        else:
            print("FAILURE: Address NOT found in footer.")

        page_desktop.screenshot(path="verification_footer.png")

        # Mobile context
        print("Verifying Mobile Button...")
        context_mobile = browser.new_context(viewport={'width': 375, 'height': 667})
        page_mobile = context_mobile.new_page()
        page_mobile.goto("http://localhost:8000/index.html")

        # Verify "Jetzt anrufen" button is visible on mobile
        # It's an anchor with "Jetzt anrufen" text inside
        call_btn = page_mobile.locator("a", has_text="Jetzt anrufen").first

        if call_btn.is_visible():
            print("SUCCESS: 'Jetzt anrufen' button is visible on mobile.")
        else:
            print("FAILURE: 'Jetzt anrufen' button is NOT visible on mobile.")

        page_mobile.screenshot(path="verification_mobile.png")

        browser.close()

if __name__ == "__main__":
    verify_changes()
