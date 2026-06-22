import os
import pytest
from playwright.sync_api import Playwright

@pytest.fixture
def page(playwright:Playwright):
    headless = os.getenv("HEADLESS", "True").lower() == "true"
    browser = playwright.chromium.launch(headless=headless,args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    # page.set_viewport_size({"width": 1536, "height": 816})
    yield page
    context.close()
    browser.close()