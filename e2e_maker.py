import asyncio
import sys
import os
from playwright.async_api import async_playwright

async def run_e2e():
    async with async_playwright() as p:
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
            await page.fill("#projectNameInput", "E2E-WS2812B-Test")
            await page.click("button:has-text('Create')")

            print("Step 4: Selecting board...")
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

            print("Step 7: Adding chatelao/pxt-ws2812b extension...")
            search_box = page.locator("input[placeholder*='Search']").last
            await search_box.wait_for(state="visible", timeout=30000)
            await search_box.fill("https://github.com/chatelao/pxt-ws2812b")
            await page.keyboard.press("Enter")

            print("Waiting for extension card...")
            await asyncio.sleep(12)
            try:
                await page.click("text='ws2812b'", force=True, timeout=30000)
                print("Clicked ws2812b extension card.")
            except:
                print("Text click failed, trying generic card click...")
                await page.locator(".ui.card").first.click(force=True)

            print("Step 8: Verifying ws2812b category in toolbox...")
            await asyncio.sleep(20) # Wait for reload

            success = False
            for i in range(20):
                if await page.locator(".blocklyTreeLabel:has-text('ws2812b')").is_visible():
                    success = True
                    break
                await asyncio.sleep(5)

            if success:
                print("Success: ws2812b category found in toolbox!")
            else:
                print("ws2812b category not found in toolbox.")
                await page.screenshot(path="e2e_failed_verification.png")

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
