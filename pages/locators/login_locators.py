from playwright.sync_api import Locator, Page

from pages.locators.base_locators import BaseLocators


class LoginLocators(BaseLocators):
    """XPath locators for the login page."""

    LOGIN_FORM = '//form[.//button[normalize-space()="Sign In"]]'
    SUBTITLE_TEXT = "Sign in to continue to your dashboard"

    def __init__(self, page: Page):
        super().__init__(page)
        self.subtitle = page.locator(
            f'xpath=//p[normalize-space()="{self.SUBTITLE_TEXT}"]'
        )
        self.email_input = page.locator(
            f"xpath={self.LOGIN_FORM}"
            '//label[contains(normalize-space(),"Email")]/following-sibling::input'
        )
        self.password_input = page.locator(
            f"xpath={self.LOGIN_FORM}"
            '//label[contains(normalize-space(),"Password")]/following-sibling::div//input'
        )
        self.sign_in_button = page.locator(
            f'xpath={self.LOGIN_FORM}//button[@type="submit" and normalize-space()="Sign In"]'
        )
        self.show_password_button = page.locator(
            f'xpath={self.LOGIN_FORM}//button[normalize-space()="Show"]'
        )
        self.hide_password_button = page.locator(
            f'xpath={self.LOGIN_FORM}//button[normalize-space()="Hide"]'
        )

    def error_message(self) -> Locator:
        return self.login_form_error()
