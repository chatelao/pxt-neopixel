import asyncio
import sys
import os
from playwright.async_api import async_playwright

async def run_e2e():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
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
            await page.locator(".card").first.click(force=True)
            print("Clicked board choice.")

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
            await asyncio.sleep(10)
            try:
                await page.click("text='neopixel'", force=True, timeout=30000)
                print("Clicked neopixel extension card.")
            except:
                await page.locator(".ui.card").first.click(force=True)

            print("Step 8: Injecting test code and switching to Blocks...")
            await asyncio.sleep(15) # Wait for reload

            # Switch to JavaScript editor
            # The toggle is often a div with role="tab" or similar text
            js_toggle = page.locator("a:has-text('JavaScript'), div:has-text('JavaScript'), button:has-text('JavaScript')").filter(has_not_text="Console").first
            await js_toggle.wait_for(state="visible", timeout=30000)
            await js_toggle.click()
            print("Switched to JavaScript.")
            await asyncio.sleep(5)

            # Use keyboard to select all and replace with neopixel code
            test_code = "let strip = neopixel.create(pins.P0, 24, NeoPixelMode.RGB);\nstrip.showColor(NeoPixelColors.Red);"
            # Focus the editor - monaco editor
            await page.click(".monaco-editor")
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.keyboard.type(test_code)
            print("Injected test code.")
            await asyncio.sleep(2)

            # Switch back to Blocks
            blocks_toggle = page.locator("a:has-text('Blocks'), div:has-text('Blocks'), button:has-text('Blocks')").first
            await blocks_toggle.click()
            print("Switched back to Blocks.")
            await asyncio.sleep(10) # Give it time to render blocks

            await page.screenshot(path="e2e_success.png")
            print("Step 9: E2E Test Completed. Screenshot saved as e2e_success.png")

        except Exception as e:
            print(f"E2E Test Failed: {e}")
            await page.screenshot(path="e2e_final_error.png")
            sys.exit(1)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_e2e())
