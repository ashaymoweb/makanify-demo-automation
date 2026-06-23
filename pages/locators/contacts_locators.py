from playwright.sync_api import Locator, Page

from pages.locators.xpath_utils import (
    button_by_text,
    error_message,
    input_by_label,
    radio_by_label,
    table_cell,
    table_header,
    textarea_by_label,
)


class ContactsLocators:
    """XPath locators for the contacts page and add-contact modal."""

    TABLE_HEADERS = (
        "Name",
        "Email",
        "Phone",
        "Gender",
        "Address line 1",
        "Address line 2",
        "Company",
        "Work email",
        "Work phone",
        "Updated",
    )
    MODAL_HEADING = "Add Contact"
    EMPTY_STATE_TEXT = "No contacts found."
    PHONE_VALIDATION_ERROR = "Enter a valid 10-digit phone number."

    CONTACTS_MAIN = '//main[.//h1[normalize-space()="Contacts"]]'
    ADD_CONTACT_MODAL = (
        '//h2[normalize-space()="Add Contact"]/ancestor::div[contains(@class,"rounded-lg")]'
    )
    SEARCH_INPUT = './/input[@placeholder="Search contacts…"]'

    def __init__(self, page: Page):
        self.page = page
        self.contacts_main = page.locator(f"xpath={self.CONTACTS_MAIN}")
        self.modal = page.locator(f"xpath={self.ADD_CONTACT_MODAL}")

        self.heading = self.contacts_main.locator(
            'xpath=.//h1[normalize-space()="Contacts"]'
        )
        self.search_input = self.contacts_main.locator(f"xpath={self.SEARCH_INPUT}")
        self.add_contact_button = button_by_text(self.contacts_main, "Add Contact")
        self.sign_out_button = page.locator(
            'xpath=//header//button[normalize-space()="Sign out"]'
        )
        self.modal_heading = self.modal.locator(
            f'xpath=.//h2[normalize-space()="{self.MODAL_HEADING}"]'
        )
        self.first_name_input = input_by_label(self.modal, "First name")
        self.last_name_input = input_by_label(self.modal, "Last name")
        self.email_input = input_by_label(self.modal, "Email")
        self.phone_input = input_by_label(self.modal, "Phone")
        self.pincode_input = input_by_label(self.modal, "PIN code")
        self.address_line1_input = textarea_by_label(self.modal, "Address line 1")
        self.address_line2_input = textarea_by_label(self.modal, "Address line 2")
        self.company_name_input = input_by_label(self.modal, "Company name")
        self.work_email_input = input_by_label(self.modal, "Work email")
        self.work_phone_input = input_by_label(self.modal, "Work phone number")
        self.save_contact_button = button_by_text(self.modal, "Save Contact")
        self.cancel_button = button_by_text(self.modal, "Cancel")
        self.empty_state = self.contacts_main.locator(
            f'xpath=.//p[normalize-space()="{self.EMPTY_STATE_TEXT}"]'
        )

    def gender_radio(self, gender: str) -> Locator:
        return radio_by_label(self.modal, "Gender", gender)

    def modal_error(self, message: str) -> Locator:
        return error_message(self.modal, message)

    def column_header(self, name: str) -> Locator:
        return table_header(self.contacts_main, name)

    def contact_cell(self, name: str) -> Locator:
        return table_cell(self.contacts_main, name)
