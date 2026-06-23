from playwright.sync_api import Locator, Page


class ContactsLocators:
    """XPath locators for the contacts page and add-contact modal."""

    TABLE_HEADERS = ("Name", "Email", "Phone", "Company", "Updated")
    MODAL_HEADING = "Add Contact"
    EMPTY_STATE_TEXT = "No contacts found."
    PHONE_VALIDATION_ERROR = "Enter a valid 10-digit phone number."

    CONTACTS_MAIN = '//main[.//h1[normalize-space()="Contacts"]]'
    ADD_CONTACT_DIALOG = (
        '//div[@role="dialog"][.//h2[normalize-space()="Add Contact"]]'
    )

    def __init__(self, page: Page):
        self.page = page
        self.heading = page.locator(
            f"xpath={self.CONTACTS_MAIN}//h1[normalize-space()='Contacts']"
        )
        self.search_input = page.locator(
            f"xpath={self.CONTACTS_MAIN}//input[@placeholder='Search contacts…']"
        )
        self.add_contact_button = page.locator(
            f"xpath={self.CONTACTS_MAIN}//button[normalize-space()='Add Contact']"
        )
        self.sign_out_button = page.locator(
            'xpath=//header//button[normalize-space()="Sign out"]'
        )
        self.modal = page.locator(f"xpath={self.ADD_CONTACT_DIALOG}")
        self.modal_heading = page.locator(
            f"xpath={self.ADD_CONTACT_DIALOG}//h2[normalize-space()='Add Contact']"
        )
        self.first_name_input = self._modal_field_input("First name")
        self.last_name_input = self._modal_field_input("Last name")
        self.email_input = self._modal_field_input("Email")
        self.phone_input = self._modal_field_input("Phone")
        self.pincode_input = self._modal_field_input("PIN code")
        self.save_contact_button = page.locator(
            f"xpath={self.ADD_CONTACT_DIALOG}//button[normalize-space()='Save Contact']"
        )
        self.cancel_button = page.locator(
            f"xpath={self.ADD_CONTACT_DIALOG}//button[normalize-space()='Cancel']"
        )
        self.empty_state = page.locator(
            f"xpath={self.CONTACTS_MAIN}//p[normalize-space()='{self.EMPTY_STATE_TEXT}']"
        )

    def _modal_field_input(self, label: str) -> Locator:
        return self.page.locator(
            f"xpath={self.ADD_CONTACT_DIALOG}"
            f'//label[contains(normalize-space(),"{label}")]/following-sibling::input'
        )

    def modal_error(self, message: str) -> Locator:
        return self.page.locator(
            f"xpath={self.ADD_CONTACT_DIALOG}//p[normalize-space()='{message}']"
        )

    def column_header(self, name: str) -> Locator:
        return self.page.locator(
            f"xpath={self.CONTACTS_MAIN}//table//th[normalize-space()='{name}']"
        )

    def contact_cell(self, name: str) -> Locator:
        return self.page.locator(
            f"xpath={self.CONTACTS_MAIN}//table//td[normalize-space()='{name}']"
        )
