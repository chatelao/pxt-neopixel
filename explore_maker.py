from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://maker.makecode.com")
    page.wait_for_timeout(5000)

    # Click "New Project"
    page.get_by_role("button", name="New Project").click()
    page.wait_for_timeout(2000)

    # Use ID for project name input
    page.locator("#projectNameInput").fill("TestProject")
    page.get_by_role("button", name="Create").click()

    # Wait for the editor to load. The URL should change to something with /#editor
    page.wait_for_url("**/#editor**", timeout=30000)
    page.wait_for_timeout(5000) # Give it some extra time to render
    page.screenshot(path="editor_loaded.png")

    # Find Extensions button - it's often in the toolbox or a menu
    # Let's try to find it by text in the toolbox
    extensions_btn = page.get_by_role("button", name="Extensions")
    if not extensions_btn.is_visible():
         # Try looking for Advanced first
         advanced_btn = page.get_by_role("button", name="Advanced")
         if advanced_btn.is_visible():
             advanced_btn.click()
             page.wait_for_timeout(1000)

    page.get_by_role("button", name="Extensions").click()
    page.wait_for_timeout(3000)
    page.screenshot(path="extensions_page.png")

    # The extensions page has a search box
    # Let's look for the search input
    search_input = page.get_by_placeholder("Search or enter project URL...")
    if search_input.is_visible():
        search_input.fill("https://github.com/chatelao/pxt-neopixel")
        search_input.press("Enter")
        page.wait_for_timeout(5000)
        page.screenshot(path="extension_search_result.png")

        # Click on the card that appears
        page.get_by_text("neopixel").first.click()
        page.wait_for_timeout(10000) # Loading extension can take time
        page.screenshot(path="after_extension_added.png")

    browser.close()
