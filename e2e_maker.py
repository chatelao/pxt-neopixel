import asyncio
import sys
import os
from playwright.async_api import async_playwright

async def run_e2e():
    async with async_playwright() as p:
        # Using a larger viewport to ensure all UI elements are visible
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        try:
            print("Step 1: Navigating to Maker MakeCode...")
            await page.goto("https://maker.makecode.com/?ignore_cache=1")

            print("Step 2: Clicking 'New Project'...")
            new_project_card = page.locator(".newprojectcard")
            await new_project_card.wait_for(state="visible", timeout=30000)
            await new_project_card.click()

            print("Step 3: Naming project...")
            await page.fill("#projectNameInput", "E2E-Neopixel-Test")
            await page.click("button:has-text('Create')")

            print("Step 4: Selecting board...")
            # Try to select Adafruit Circuit Playground Express specifically for consistent block availability
            try:
                board_card = page.locator(".card:has-text('Adafruit Circuit Playground Express')").first
                await board_card.wait_for(state="visible", timeout=15000)
                await board_card.click(force=True)
                print("Selected Adafruit Circuit Playground Express.")
            except:
                print("Adafruit board not found, selecting first available board.")
                await page.locator(".card").first.click(force=True)

            print("Step 5: Waiting for editor to load...")
            await page.wait_for_selector(".blocklyTreeRow", timeout=60000)

            print("Step 6: Opening Extensions...")
            ext_label = page.locator(".blocklyTreeLabel:has-text('Extensions')")
            if not await ext_label.is_visible():
                print("Expanding Advanced...")
                await page.locator(".blocklyTreeLabel:has-text('Advanced')").click(force=True)
                await asyncio.sleep(2)

            await ext_label.scroll_into_view_if_needed()
            await ext_label.click(force=True)

            print("Step 7: Adding chatelao/pxt-neopixel extension...")
            search_box = page.locator("input[placeholder*='Search']").last
            await search_box.wait_for(state="visible", timeout=30000)
            await search_box.fill("https://github.com/chatelao/pxt-neopixel")
            await page.keyboard.press("Enter")

            print("Waiting for extension card...")
            # Increased wait for search results
            await asyncio.sleep(12)
            try:
                # Based on previous runs, clicking by text is reliable once found
                await page.click("text='neopixel'", force=True, timeout=30000)
                print("Clicked neopixel extension card.")
            except:
                print("Text click failed, trying generic card click...")
                await page.locator(".ui.card").first.click(force=True)

            print("Step 8: Injecting test code...")
            await asyncio.sleep(20) # Long wait for project reload after extension addition

            # Use a more reliable way to find the JS toggle
            # In PXT, it's often a button with id="javascriptEditorMenuItem" or similar
            # Or just look for the text in the main header
            js_toggle = page.locator("button:has-text('JavaScript'), a:has-text('JavaScript')").first
            await js_toggle.wait_for(state="visible", timeout=30000)
            await js_toggle.click()
            print("Switched to JavaScript editor.")
            await asyncio.sleep(8)

            # Select all and delete current code
            await page.click(".monaco-editor")
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")

            # Inject code that translates clearly to blocks in 'on start'
            # pins.P0 is standard for many maker boards
            test_code = """let strip = neopixel.create(pins.P0, 24, NeoPixelMode.RGB)
strip.setPixelColor(0, NeoPixelColors.Red)
"""
            await page.keyboard.type(test_code)
            print("Injected test code.")
            await asyncio.sleep(5)

            print("Step 9: Switching back to Blocks view...")
            blocks_toggle = page.locator("button:has-text('Blocks'), a:has-text('Blocks')").first
            await blocks_toggle.click()
            print("Switched to Blocks.")
            await asyncio.sleep(15) # Wait for blocks to render

            # Final screenshot
            await page.screenshot(path="e2e_success.png")
            print("Step 10: E2E Test Completed. Screenshot saved as e2e_success.png")

        except Exception as e:
            print(f"E2E Test Failed: {e}")
            await page.screenshot(path="e2e_final_error.png")
            sys.exit(1)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_e2e())
