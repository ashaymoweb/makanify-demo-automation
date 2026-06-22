import os

from playwright.sync_api import Page, expect

from pages.BasePage import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.show_password_button = page.get_by_role("button", name="Show")
        self.hide_password_button = page.get_by_role("button", name="Hide")
        self.subtitle = page.get_by_text("Sign in to continue to your dashboard")

    def open_login(self) -> None:
        self.open("/login")
        expect(self.subtitle).to_be_visible()

    def fill_email(self, email: str) -> None:
        self.email_input.fill(email)

    def fill_password(self, password: str) -> None:
        self.password_input.fill(password)

    def clear_email(self) -> None:
        self.email_input.clear()

    def clear_password(self) -> None:
        self.password_input.clear()

    def click_sign_in(self) -> None:
        self.sign_in_button.click()

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
        self.show_password_button.click()

    def hide_password(self) -> None:
        self.hide_password_button.click()

    def expect_sign_in_disabled(self) -> None:
        expect(self.sign_in_button).to_be_disabled()

    def expect_sign_in_enabled(self) -> None:
        expect(self.sign_in_button).to_be_enabled()

    def expect_on_login_page(self) -> None:
        self.expect_url("/login")
        expect(self.subtitle).to_be_visible()

    def expect_password_hidden(self) -> None:
        expect(self.password_input).to_have_attribute("type", "password")

    def expect_password_visible(self) -> None:
        expect(self.password_input).to_have_attribute("type", "text")

    def expect_show_button_visible(self) -> None:
        expect(self.show_password_button).to_be_visible()

    def expect_hide_button_visible(self) -> None:
        expect(self.hide_password_button).to_be_visible()
