from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto('http://localhost:8000')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='d:/AITEST/novel-weaver/web/screenshot.png', full_page=True)
    print("Screenshot saved to d:/AITEST/novel-weaver/web/screenshot.png")
    browser.close()
