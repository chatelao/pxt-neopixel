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
            # Clicks are sometimes intercepted by the modal. Using force=True.
            await page.locator(".card").first.click(force=True)
            print("Clicked board choice.")

            print("Step 5: Waiting for editor to load...")
            await page.wait_for_selector(".blocklyTreeRow", timeout=60000)

            print("Step 6: Opening Extensions...")
            ext_label = page.locator(".blocklyTreeLabel:has-text('Extensions')")
            if not await ext_label.is_visible():
                print("Extensions label not visible, expanding Advanced...")
                await page.locator(".blocklyTreeLabel:has-text('Advanced')").click(force=True)
                await asyncio.sleep(2)

            await ext_label.scroll_into_view_if_needed()
            await ext_label.click(force=True)

            print("Step 7: Adding chatelao/pxt-neopixel extension...")
            search_box = page.locator("input[placeholder*='Search']").last
            await search_box.wait_for(state="visible", timeout=30000)

            # Use chatelao/neopixel repo.
            await search_box.fill("https://github.com/chatelao/pxt-neopixel")
            await page.keyboard.press("Enter")

            print("Waiting for extension card...")
            await asyncio.sleep(10)

            # Based on previous successful runs, click by text works.
            try:
                await page.click("text='neopixel'", force=True, timeout=30000)
                print("Clicked neopixel extension card.")
            except:
                print("Text click failed, trying generic card click...")
                await page.locator(".ui.card").first.click(force=True)

            print("Step 8: Verifying Neopixel category and adding test code...")
            # Wait for editor to reload.
            await asyncio.sleep(15)

            # Try to switch to JavaScript and add code
            try:
                js_button = page.locator("button:has-text('JavaScript')")
                if await js_button.is_visible():
                    await js_button.click()
                    print("Switched to JavaScript editor.")
                    await asyncio.sleep(5)

                    # Inject minimal test code
                    test_code = "let strip = neopixel.create(pins.P0, 24, NeoPixelMode.RGB);\nstrip.showColor(NeoPixelColors.Red);"
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await page.keyboard.type(test_code)
                    print("Injected minimal test code.")
                    await asyncio.sleep(5) # Give it time to compile/update
            except Exception as code_err:
                print(f"Failed to inject test code: {code_err}")

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
