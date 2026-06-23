import pytest

from pages.ContactsPage import ContactsPage
from pages.LoginPage import LoginPage
from utilities.random_data_generator import RandomDataGenerator


@pytest.mark.contacts
@pytest.mark.positive
def test_contacts_pos_001_contacts_page_loads_with_table(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()
    contacts_page.expect_table_headers()


@pytest.mark.contacts
@pytest.mark.positive
def test_contacts_pos_002_add_contact_with_valid_data(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()

    first_name = RandomDataGenerator.random_first_name()
    last_name = RandomDataGenerator.random_last_name()
    phone = RandomDataGenerator.random_indian_mobile()
    pin_code = RandomDataGenerator.random_pincode()

    contacts_page.open_add_contact_modal()
    contacts_page.fill_contact_form(
        first_name=first_name,
        last_name=last_name,
        email=RandomDataGenerator.random_email(),
        phone=phone,
        pin_code=pin_code,
    )
    contacts_page.submit_contact_form()
    contacts_page.expect_modal_closed()
    contacts_page.expect_contact_in_table(f"{first_name} {last_name}")


@pytest.mark.contacts
@pytest.mark.positive
def test_contacts_pos_003_search_filters_existing_contact(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()

    first_name = RandomDataGenerator.random_first_name()
    last_name = RandomDataGenerator.random_last_name()

    contacts_page.open_add_contact_modal()
    contacts_page.fill_contact_form(
        first_name=first_name,
        last_name=last_name,
        phone=RandomDataGenerator.random_indian_mobile(),
        pin_code=RandomDataGenerator.random_pincode(),
    )
    contacts_page.submit_contact_form()
    contacts_page.expect_contact_in_table(f"{first_name} {last_name}")

    contacts_page.search(first_name)
    contacts_page.expect_contact_in_table(f"{first_name} {last_name}")


@pytest.mark.contacts
@pytest.mark.positive
def test_contacts_pos_004_cancel_add_contact_closes_modal(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()

    contacts_page.open_add_contact_modal()
    contacts_page.fill_contact_form(
        first_name="Cancel",
        last_name="Test",
        phone=RandomDataGenerator.random_indian_mobile(),
        pin_code=RandomDataGenerator.random_pincode(),
    )
    contacts_page.cancel_add_contact()


@pytest.mark.contacts
@pytest.mark.positive
def test_contacts_pos_005_add_contact_with_required_fields_only(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()

    first_name = RandomDataGenerator.random_first_name()
    phone = RandomDataGenerator.random_indian_mobile()
    pin_code = RandomDataGenerator.random_pincode()

    contacts_page.open_add_contact_modal()
    contacts_page.fill_contact_form(
        first_name=first_name,
        phone=phone,
        pin_code=pin_code,
    )
    contacts_page.submit_contact_form()
    contacts_page.expect_modal_closed()
    contacts_page.expect_contact_in_table(first_name)


@pytest.mark.contacts
@pytest.mark.positive
def test_contacts_pos_006_add_contact_button_opens_modal(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()

    contacts_page.open_add_contact_modal()
    contacts_page.expect_modal_open()


@pytest.mark.contacts
@pytest.mark.negative
def test_contacts_neg_001_search_with_no_matches_shows_empty_state(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()

    contacts_page.search("zzz-nonexistent-contact-99999")
    contacts_page.expect_no_contacts_found()


@pytest.mark.contacts
@pytest.mark.negative
def test_contacts_neg_003_short_phone_number_shows_validation_error(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()

    contacts_page.open_add_contact_modal()
    contacts_page.fill_contact_form(
        first_name="Short",
        phone="12345",
        pin_code=RandomDataGenerator.random_pincode(),
    )
    contacts_page.submit_contact_form()
    contacts_page.expect_phone_validation_error()
    contacts_page.expect_modal_open()


@pytest.mark.contacts
@pytest.mark.negative
def test_contacts_neg_002_submit_without_first_name_keeps_modal_open(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()

    contacts_page.open_add_contact_modal()
    contacts_page.fill_contact_form(
        phone=RandomDataGenerator.random_indian_mobile(),
        pin_code=RandomDataGenerator.random_pincode(),
    )
    contacts_page.submit_contact_form()
    contacts_page.expect_modal_open()
