import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright

load_dotenv(".env.test")

@pytest.fixture
def page(playwright: Playwright):
    headless = os.getenv("HEADLESS", "TRUE").lower() == "true"

    browser = playwright.chromium.launch(
        headless=headless,
        slow_mo=1000,
        args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    yield page

    context.close()
    browser.close()