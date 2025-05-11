"""
DEPRECATED: This file is no longer in use and will be removed in a future version.
"""

import time
import warnings

from playwright.sync_api import sync_playwright

warnings.warn(
    "The module 'code_classifier' is deprecated and will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2
)


def get_code_content_size() -> tuple[int, int]:
    """
    Retrieves the dimensions of the code container element from a locally hosted HTML page.
    
    Uses Playwright to launch a headless browser, navigate to a local HTML page,
    and measure the dimensions of the code container element.
    
    Returns:
        tuple[int, int]: A tuple containing the width and height of the code container in pixels.
                         Returns (800, 600) as fallback if the element cannot be found or accessed.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Retry logic for server connection
        max_retries = 3
        for _ in range(max_retries):
            try:
                page.goto("http://localhost:55003/resources/temp.html", timeout=5000)
                break
            except:
                time.sleep(1)
                continue

        # Get width and height of the code-content element
        code_content = page.query_selector(".code-container")
        if code_content:
            width = round(code_content.bounding_box()["width"])
            height = round(code_content.bounding_box()["height"])
            browser.close()
            return width, height

        browser.close()
        return 800, 600
