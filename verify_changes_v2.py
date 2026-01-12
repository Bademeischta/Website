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

        # Verify "Jetzt anrufen" button (anchor) is visible on mobile
        # We check by href because the text might be hidden
        call_btn = page_mobile.locator('a[href="tel:0123456789"]').first

        if call_btn.is_visible():
            print("SUCCESS: 'Jetzt anrufen' button is visible on mobile.")
            # Check if text is hidden (optional, but good to know)
            text_span = call_btn.locator("span").last
            if not text_span.is_visible():
                print("INFO: Button text is hidden on mobile (Icon only), as expected.")
            else:
                print("INFO: Button text is visible on mobile.")
        else:
            print("FAILURE: 'Jetzt anrufen' button is NOT visible on mobile.")

        page_mobile.screenshot(path="verification_mobile_v2.png")

        browser.close()

if __name__ == "__main__":
    verify_changes()
