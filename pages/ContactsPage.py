from playwright.sync_api import Page, expect

from pages.BasePage import BasePage
from pages.locators.contacts_locators import ContactsLocators


class ContactsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = ContactsLocators(page)

    def open_contacts(self) -> None:
        self.open("/contacts")

    def expect_loaded(self) -> None:
        self.expect_url("/contacts")
        expect(self.locators.heading).to_be_visible()
        expect(self.locators.add_contact_button).to_be_visible()

    def expect_table_headers(self) -> None:
        for header in ContactsLocators.TABLE_HEADERS:
            expect(self.locators.column_header(header)).to_be_visible()

    def search(self, query: str) -> None:
        with self.page.expect_response(
            lambda response: "/contact" in response.url
            and response.request.method == "GET"
            and "search=" in response.url,
            timeout=15000,
        ):
            self.locators.search_input.fill(query)

    def open_add_contact_modal(self) -> None:
        self.locators.add_contact_button.click()
        self.expect_modal_open()

    def fill_contact_form(
        self,
        *,
        first_name: str = "",
        last_name: str = "",
        email: str = "",
        phone: str = "",
        pin_code: str = "",
        gender: str = "",
    ) -> None:
        if first_name:
            self.locators.first_name_input.fill(first_name)
        if last_name:
            self.locators.last_name_input.fill(last_name)
        if email:
            self.locators.email_input.fill(email)
        if phone:
            self.locators.phone_input.fill(phone)
        if pin_code:
            self.locators.pincode_input.fill(pin_code)
        if gender:
            self.locators.gender_radio(gender).check()

    def select_gender(self, gender: str) -> None:
        self.locators.gender_radio(gender).check()

    def submit_contact_form(self) -> None:
        self.locators.save_contact_button.click()

    def cancel_add_contact(self) -> None:
        self.locators.cancel_button.click()
        self.expect_modal_closed()

    def expect_modal_open(self) -> None:
        expect(self.locators.modal_heading).to_be_visible()
        expect(self.locators.first_name_input).to_be_visible()
        expect(self.locators.gender_radio("Male")).to_be_checked()

    def expect_modal_closed(self) -> None:
        expect(self.locators.modal_heading).to_be_hidden()

    def expect_phone_validation_error(self) -> None:
        expect(
            self.locators.modal_error(ContactsLocators.PHONE_VALIDATION_ERROR)
        ).to_be_visible()

    def expect_contact_in_table(self, name: str, timeout: int = 20000) -> None:
        expect(self.locators.contact_cell(name)).to_be_visible(timeout=timeout)

    def expect_no_contacts_found(self, timeout: int = 15000) -> None:
        spinner = self.locators.contacts_main.locator(
            "xpath=.//div[contains(@class,'animate-spin')]"
        )
        expect(spinner).to_be_hidden(timeout=timeout)
        expect(self.locators.empty_state).to_be_visible(timeout=timeout)

    def sign_out(self) -> None:
        self.locators.sign_out_button.click()
