import os

from playwright.sync_api import Page, expect

from pages.BasePage import BasePage
from pages.locators.login_locators import LoginLocators


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = LoginLocators(page)

    def open_login(self) -> None:
        self.open("/login")
        expect(self.locators.subtitle).to_be_visible()

    def fill_email(self, email: str) -> None:
        self.locators.email_input.fill(email)

    def fill_password(self, password: str) -> None:
        self.locators.password_input.fill(password)

    def clear_email(self) -> None:
        self.locators.email_input.clear()

    def clear_password(self) -> None:
        self.locators.password_input.clear()

    def click_sign_in(self) -> None:
        self.locators.sign_in_button.click()

    def login(self, email: str, password: str) -> None:
        self.fill_email(email)
        self.fill_password(password)
        self.click_sign_in()

    def login_with_valid_credentials(self) -> None:
        """Single reusable login entry point for all authenticated test scenarios."""
        self.open_login()
        email = os.getenv("TEST_EMAIL", "")
        password = os.getenv("TEST_PASSWORD", "")
        if not email or not password:
            raise RuntimeError(
                "Set TEST_EMAIL and TEST_PASSWORD environment variables before running tests."
            )
        self.login(email, password)

    def show_password(self) -> None:
        self.locators.show_password_button.click()

    def hide_password(self) -> None:
        self.locators.hide_password_button.click()

    def expect_sign_in_disabled(self) -> None:
        expect(self.locators.sign_in_button).to_be_disabled()

    def expect_sign_in_enabled(self) -> None:
        expect(self.locators.sign_in_button).to_be_enabled()

    def expect_on_login_page(self) -> None:
        self.expect_url("/login")
        expect(self.locators.subtitle).to_be_visible()

    def expect_password_hidden(self) -> None:
        expect(self.locators.password_input).to_have_attribute("type", "password")

    def expect_password_visible(self) -> None:
        expect(self.locators.password_input).to_have_attribute("type", "text")

    def expect_show_button_visible(self) -> None:
        expect(self.locators.show_password_button).to_be_visible()

    def expect_hide_button_visible(self) -> None:
        expect(self.locators.hide_password_button).to_be_visible()

    def expect_any_error(self, timeout: int = 15000) -> None:
        expect(self.locators.error_message()).to_be_visible(timeout=timeout)
