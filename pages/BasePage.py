import os

from playwright.sync_api import Page, expect


class BasePage:
    """Shared Playwright helpers for the Makanify demo frontend."""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = os.getenv("BASE_URL", "http://localhost:3000").rstrip("/")

    def open(self, path: str = "/") -> None:
        self.page.goto(f"{self.base_url}{path}")

    def expect_url(self, path: str, timeout: int = 15000) -> None:
        expect(self.page).to_have_url(f"{self.base_url}{path}", timeout=timeout)

    def expect_error_message(self, message: str, timeout: int = 15000) -> None:
        locator = self.page.locator("p.text-red-600")
        expect(locator).to_be_visible(timeout=timeout)
        if message:
            expect(locator).to_contain_text(message, timeout=timeout)

    def expect_any_error(self, timeout: int = 15000) -> None:
        expect(self.page.locator("p.text-red-600")).to_be_visible(timeout=timeout)
