from playwright.sync_api import Locator, Page


class BaseLocators:
    """Shared XPath locators used across multiple pages."""

    LOGIN_FORM_ERROR_XPATH = (
        'xpath=//form[.//button[normalize-space()="Sign In"]]'
        "//p[contains(@class,'text-red-600')]"
    )

    def __init__(self, page: Page):
        self.page = page

    def login_form_error(self) -> Locator:
        return self.page.locator(self.LOGIN_FORM_ERROR_XPATH)
