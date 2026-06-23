from playwright.sync_api import Locator, Page

from pages.locators.xpath_utils import button_by_text, input_by_label
from pages.locators.base_locators import BaseLocators


class LoginLocators(BaseLocators):
    """XPath locators for the login page."""

    SUBTITLE_TEXT = "Sign in to continue to your dashboard"

    def __init__(self, page: Page):
        super().__init__(page)
        self.subtitle = page.locator(
            f'xpath=//p[normalize-space()="{self.SUBTITLE_TEXT}"]'
        )
        self.email_input = input_by_label(self.login_form, "Email")
        self.password_input = input_by_label(self.login_form, "Password")
        self.sign_in_button = button_by_text(self.login_form, "Sign In")
        self.show_password_button = button_by_text(self.login_form, "Show")
        self.hide_password_button = button_by_text(self.login_form, "Hide")

    def error_message(self) -> Locator:
        return self.login_form.locator("xpath=.//p[contains(@class,'text-red-600')]")
