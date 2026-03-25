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
            # It's better to find the Extensions category label specifically.
            ext_label = page.locator(".blocklyTreeLabel:has-text('Extensions')")
            if not await ext_label.is_visible():
                print("Extensions label not visible, expanding Advanced...")
                await page.locator(".blocklyTreeLabel:has-text('Advanced')").click(force=True)
                await asyncio.sleep(2)

            await ext_label.scroll_into_view_if_needed()
            await ext_label.click(force=True)

            print("Step 7: Adding Neopixel extension...")
            # Wait for any search input to appear in the gallery.
            search_box = page.locator("input[placeholder*='Search']").last
            await search_box.wait_for(state="visible", timeout=30000)

            # Use current repo URL.
            await search_box.fill("https://github.com/microsoft/pxt-neopixel")
            await page.keyboard.press("Enter")

            print("Waiting for extension card...")
            await asyncio.sleep(10)

            # Based on e2e_error_card_click.png, the card is present.
            # Try to locate by its unique content or tag.
            # It's likely a div with class 'ui card' or similar.
            # The word 'neopixel' is definitely in it.
            neopixel_card = page.locator("div.ui.card:has-text('neopixel')").first
            try:
                await neopixel_card.wait_for(state="visible", timeout=30000)
                print("Found card, clicking...")
                await neopixel_card.click(force=True)
            except Exception as e:
                print(f"Failed to find Neopixel cardspecifically: {e}")
                # Fallback to text click.
                await page.click("text='neopixel'", force=True)
                print("Clicked by text fallback.")

            print("Step 8: Verifying Neopixel category in toolbox...")
            success = False
            for i in range(20):
                if await page.locator(".blocklyTreeLabel:has-text('Neopixel')").is_visible() or \
                   await page.locator(".blocklyTreeLabel:has-text('NeoPixel')").is_visible():
                    success = True
                    break
                await asyncio.sleep(5)

            if success:
                print("Success: Neopixel category found in toolbox!")
            else:
                print("Neopixel category not found in toolbox within the verification timeout.")
                await page.screenshot(path="e2e_failed_toolbox_verification.png")

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
