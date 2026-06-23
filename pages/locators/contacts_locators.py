from playwright.sync_api import Locator, Page


class ContactsLocators:
    """Centralized locators for the contacts page and add-contact modal."""

    TABLE_HEADERS = ("Name", "Email", "Phone", "Company", "Updated")
    MODAL_HEADING = "Add Contact"
    EMPTY_STATE_TEXT = "No contacts found."
    PHONE_VALIDATION_ERROR = "Enter a valid 10-digit phone number."
    MODAL_ROOT_XPATH = "xpath=//h2[normalize-space()='Add Contact']/parent::div"

    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Contacts")
        self.search_input = page.get_by_placeholder("Search contacts…")
        self.add_contact_button = page.get_by_role("button", name="Add Contact")
        self.sign_out_button = page.get_by_role("button", name="Sign out")
        self.modal_heading = page.get_by_role("heading", name=self.MODAL_HEADING)
        self.modal = page.locator(self.MODAL_ROOT_XPATH)
        self.first_name_input = self.modal.get_by_label("First name", exact=False)
        self.last_name_input = self.modal.get_by_label("Last name", exact=False)
        self.email_input = self.modal.get_by_label("Email", exact=False)
        self.phone_input = self.modal.get_by_label("Phone", exact=False)
        self.pincode_input = self.modal.get_by_label("PIN code", exact=False)
        self.save_contact_button = self.modal.get_by_role("button", name="Save Contact")
        self.cancel_button = self.modal.get_by_role("button", name="Cancel")
        self.empty_state = page.get_by_text(self.EMPTY_STATE_TEXT)

    def modal_error(self, message: str) -> Locator:
        return self.modal.get_by_text(message)

    def column_header(self, name: str) -> Locator:
        return self.page.get_by_role("columnheader", name=name)

    def contact_cell(self, name: str) -> Locator:
        return self.page.get_by_role("cell", name=name)
