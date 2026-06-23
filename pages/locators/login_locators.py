from playwright.sync_api import Locator, Page

from pages.locators.base_locators import BaseLocators


class LoginLocators(BaseLocators):
    """Centralized locators for the login page."""

    SUBTITLE_TEXT = "Sign in to continue to your dashboard"

    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.show_password_button = page.get_by_role("button", name="Show")
        self.hide_password_button = page.get_by_role("button", name="Hide")
        self.subtitle = page.get_by_text(self.SUBTITLE_TEXT)

    def error_message(self) -> Locator:
        return self.login_form_error()
