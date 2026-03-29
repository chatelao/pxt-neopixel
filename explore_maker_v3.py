import asyncio
from playwright.async_api import async_playwright

async def explore():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        print("Navigating to maker.makecode.com...")
        await page.goto("https://maker.makecode.com/?ignore_cache=1")

        # Wait for the "New Project" card
        print("Waiting for New Project card...")
        new_project_card = page.locator(".newprojectcard")
        await new_project_card.wait_for(state="visible", timeout=30000)

        print("Clicking New Project...")
        await new_project_card.click()

        # Fill project name
        print("Entering project name...")
        await page.fill("#projectNameInput", "TestProject")

        # Click Create
        print("Clicking Create...")
        await page.click("button:has-text('Create')")

        # Wait for board selection - this might appear as a modal or new view
        print("Waiting for board selection...")
        try:
            # Try to find Raspberry Pi Pico card
            # Using a more robust selector
            board_selector = "div.card[aria-label='Raspberry Pi Pico']"
            await page.wait_for_selector(board_selector, timeout=15000)
            print("Selecting Raspberry Pi Pico...")
            await page.click(board_selector)
        except Exception as e:
            print(f"Board selection failed or not found: {e}")
            await page.screenshot(path="board_selection_error_v3.png")

        # Wait for editor to load
        print("Waiting for editor...")
        try:
            await page.wait_for_selector(".blocklyWorkspace", timeout=30000)
            print("Editor loaded!")
        except Exception as e:
            print(f"Editor did not load: {e}")
            await page.screenshot(path="editor_error_v3.png")
            # Maybe it's already loaded or has different class

        await page.screenshot(path="editor_v3.png")

        # Look for Extensions
        print("Looking for Extensions button...")
        # MakeCode editor toolbox uses blocklyTreeLabel
        try:
            # Sometimes it's better to use text in the toolbox
            # Try scrolling the toolbox if needed, but usually it's visible
            extensions_selector = "text=Extensions"
            # It might be at the bottom, try to scroll it into view
            ext_label = page.locator(".blocklyTreeLabel:has-text('Extensions')")
            if await ext_label.count() == 0:
                print("Extensions not found, trying Advanced...")
                advanced_label = page.locator(".blocklyTreeLabel:has-text('Advanced')")
                await advanced_label.click()
                await asyncio.sleep(1)

            await ext_label.scroll_into_view_if_needed()
            await ext_label.click()
            print("Clicked Extensions!")
        except Exception as e:
            print(f"Failed to find/click Extensions: {e}")
            await page.screenshot(path="toolbox_v3.png")

        # Extensions dialog
        try:
            search_selector = "input[placeholder='Search or enter project URL...']"
            await page.wait_for_selector(search_selector, timeout=10000)
            print("Extensions dialog opened!")
            await page.fill(search_selector, "https://github.com/microsoft/pxt-neopixel")
            await page.keyboard.press("Enter")

            print("Searching for extension...")
            # Wait for the card. The label might be "pxt-neopixel"
            card_selector = "div.ui.card" # We'll find the one with the right text
            await page.wait_for_selector(card_selector, timeout=15000)

            # Click the one that looks like our repo
            target_card = page.locator("div.ui.card:has-text('pxt-neopixel')")
            await target_card.first.click()

            print("Clicked extension card. Waiting for it to be added...")
            await asyncio.sleep(10)
            await page.screenshot(path="final_v3.png")
            print("SUCCESS")
        except Exception as e:
            print(f"Failed in extension dialog: {e}")
            await page.screenshot(path="extension_error_v3.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(explore())
