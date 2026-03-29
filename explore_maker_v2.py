import asyncio
from playwright.async_api import async_playwright

async def explore():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        print("Navigating to maker.makecode.com...")
        await page.goto("https://maker.makecode.com/?ignore_cache=1")

        # Click "New Project"
        print("Clicking New Project...")
        await page.click("text=New Project")

        # Fill project name
        print("Entering project name...")
        await page.fill("#projectNameInput", "TestProject")

        # Click Create
        print("Clicking Create...")
        await page.click("button:has-text('Create')")

        # Wait for board selection
        print("Waiting for board selection...")
        try:
            # Wait for Raspberry Pi Pico card
            await page.wait_for_selector("div[aria-label='Raspberry Pi Pico']", timeout=10000)
            print("Selecting Raspberry Pi Pico...")
            await page.click("div[aria-label='Raspberry Pi Pico']")
        except Exception as e:
            print(f"Board selection failed or not found: {e}")
            await page.screenshot(path="board_selection_error.png")

        # Wait for editor to load
        print("Waiting for editor...")
        await page.wait_for_selector(".blocklyWorkspace", timeout=30000)
        print("Editor loaded!")

        await page.screenshot(path="editor_actual.png")

        # Look for Extensions in the toolbox
        # Usually it's at the bottom of the toolbox
        print("Looking for Extensions button...")
        try:
            # In MakeCode, Extensions is often a tree item in the toolbox
            extensions_selector = ".blocklyTreeLabel:has-text('Extensions')"
            await page.wait_for_selector(extensions_selector, timeout=10000)
            print("Found Extensions button!")
            await page.click(extensions_selector)
        except Exception as e:
            print(f"Extensions button not found directly: {e}")
            # Try clicking "Advanced" first if it exists
            try:
                advanced_selector = ".blocklyTreeLabel:has-text('Advanced')"
                print("Trying to click Advanced...")
                await page.click(advanced_selector)
                await page.wait_for_selector(extensions_selector, timeout=5000)
                print("Found Extensions button under Advanced!")
                await page.click(extensions_selector)
            except Exception as e2:
                print(f"Advanced/Extensions not found: {e2}")
                await page.screenshot(path="toolbox_error.png")

        # If Extensions dialog opens, look for the search box
        try:
            search_selector = "input[placeholder='Search or enter project URL...']"
            await page.wait_for_selector(search_selector, timeout=10000)
            print("Extensions dialog opened!")
            await page.fill(search_selector, "https://github.com/microsoft/pxt-neopixel")
            await page.keyboard.press("Enter")

            # Wait for the card to appear and click it
            card_selector = "div.ui.card[aria-label*='pxt-neopixel']"
            await page.wait_for_selector(card_selector, timeout=15000)
            print("Found pxt-neopixel extension card!")
            await page.click(card_selector)

            print("Clicked extension card. Waiting for it to be added...")
            # Extension addition can take time and might reload parts of the UI
            await asyncio.sleep(10)
            await page.screenshot(path="final_state.png")
            print("Finished E2E flow.")
        except Exception as e:
            print(f"Failed to add extension: {e}")
            await page.screenshot(path="extension_error.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(explore())
