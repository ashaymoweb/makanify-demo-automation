from playwright.sync_api import Locator, Page


class BaseLocators:
    """Shared container XPath constants and cross-page locators."""

    LOGIN_FORM = '//form[.//button[normalize-space()="Sign In"]]'

    def __init__(self, page: Page):
        self.page = page
        self.login_form = page.locator(f"xpath={self.LOGIN_FORM}")

    def login_form_error(self) -> Locator:
        return self.login_form.locator("xpath=.//p[contains(@class,'text-red-600')]")
