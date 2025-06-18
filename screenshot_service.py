import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse, urljoin
import os

async def take_screenshots_of_all_links_api(main_url: str, output_folder: str):
    screenshots = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(main_url, wait_until="networkidle")
        # Screenshot the main page
        main_screenshot = os.path.join(output_folder, "screenshot_main.png")
        await page.screenshot(path=main_screenshot, full_page=True)
        screenshots.append(main_screenshot)
        # Extract all unique hrefs from <a> tags (absolute and relative)
        hrefs = await page.eval_on_selector_all(
            "a[href]", "elements => Array.from(new Set(elements.map(e => e.getAttribute('href'))))"
        )
        # Convert relative URLs to absolute URLs and filter for same domain
        main_netloc = urlparse(main_url).netloc
        absolute_hrefs = []
        for href in hrefs:
            if not href:
                continue
            abs_url = urljoin(main_url, href)
            if urlparse(abs_url).scheme.startswith("http") and urlparse(abs_url).netloc == main_netloc and abs_url != main_url:
                absolute_hrefs.append(abs_url)
        # Remove duplicates
        absolute_hrefs = list(dict.fromkeys(absolute_hrefs))
        # Visit and screenshot each linked page
        for i, href in enumerate(absolute_hrefs, 1):
            try:
                new_page = await context.new_page()
                await new_page.goto(href, wait_until="networkidle")
                await asyncio.sleep(5)
                screenshot_path = os.path.join(output_folder, f"screenshot_{i}.png")
                await new_page.screenshot(path=screenshot_path, full_page=True)
                await new_page.close()
                screenshots.append(screenshot_path)
            except Exception as e:
                print(f"❌ Failed to screenshot {href}: {e}")
        await browser.close()
    return screenshots 