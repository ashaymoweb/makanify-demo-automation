from playwright.sync_api import Page, expect

from pages.BasePage import BasePage


class ContactsPage(BasePage):
    TABLE_HEADERS = ("Name", "Email", "Phone", "Company", "Updated")

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Contacts")
        self.search_input = page.get_by_placeholder("Search contacts…")
        self.add_contact_button = page.get_by_role("button", name="Add Contact")
        self.sign_out_button = page.get_by_role("button", name="Sign out")
        self.modal_heading = page.get_by_role("heading", name="Add Contact")
        self.modal = page.locator("div").filter(has=self.modal_heading)
        self.first_name_input = self.modal.get_by_label("First name", exact=False)
        self.last_name_input = self.modal.get_by_label("Last name", exact=False)
        self.email_input = self.modal.get_by_label("Email", exact=False)
        self.phone_input = self.modal.get_by_label("Phone", exact=False)
        self.pincode_input = self.modal.get_by_label("PIN code", exact=False)
        self.save_contact_button = self.modal.get_by_role(
            "button", name="Save Contact"
        )
        self.cancel_button = self.modal.get_by_role("button", name="Cancel")

    def open_contacts(self) -> None:
        self.open("/contacts")

    def expect_loaded(self) -> None:
        self.expect_url("/contacts")
        expect(self.heading).to_be_visible()
        expect(self.add_contact_button).to_be_visible()

    def expect_table_headers(self) -> None:
        for header in self.TABLE_HEADERS:
            expect(self.page.get_by_role("columnheader", name=header)).to_be_visible()

    def search(self, query: str) -> None:
        with self.page.expect_response(
            lambda response: "/contact" in response.url
            and response.request.method == "GET"
        ):
            self.search_input.fill(query)

    def open_add_contact_modal(self) -> None:
        self.add_contact_button.click()
        self.expect_modal_open()

    def fill_contact_form(
        self,
        *,
        first_name: str = "",
        last_name: str = "",
        email: str = "",
        phone: str = "",
        pin_code: str = "",
    ) -> None:
        if first_name:
            self.first_name_input.fill(first_name)
        if last_name:
            self.last_name_input.fill(last_name)
        if email:
            self.email_input.fill(email)
        if phone:
            self.phone_input.fill(phone)
        if pin_code:
            self.pincode_input.fill(pin_code)

    def submit_contact_form(self) -> None:
        self.save_contact_button.click()

    def cancel_add_contact(self) -> None:
        self.cancel_button.click()
        self.expect_modal_closed()

    def expect_modal_open(self) -> None:
        expect(self.modal_heading).to_be_visible()

    def expect_modal_closed(self) -> None:
        expect(self.modal_heading).to_be_hidden()

    def expect_contact_in_table(self, name: str, timeout: int = 20000) -> None:
        expect(self.page.get_by_role("cell", name=name).first).to_be_visible(
            timeout=timeout
        )

    def expect_no_contacts_found(self, timeout: int = 15000) -> None:
        expect(self.page.get_by_text("No contacts found.")).to_be_visible(timeout=timeout)

    def sign_out(self) -> None:
        self.sign_out_button.click()
