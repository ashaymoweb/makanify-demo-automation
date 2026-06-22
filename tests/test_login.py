import pytest

from pages.ContactsPage import ContactsPage
from pages.LoginPage import LoginPage


@pytest.mark.login
@pytest.mark.positive
def test_login_pos_001_successful_login_with_valid_credentials(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()


@pytest.mark.login
@pytest.mark.positive
def test_login_pos_002_show_password_toggle_reveals_password(page):
    login_page = LoginPage(page)
    login_page.open_login()
    login_page.fill_password("secret")
    login_page.expect_password_hidden()
    login_page.show_password()
    login_page.expect_password_visible()
    login_page.expect_hide_button_visible()


@pytest.mark.login
@pytest.mark.positive
def test_login_pos_003_hide_password_toggle_masks_password(page):
    login_page = LoginPage(page)
    login_page.open_login()
    login_page.fill_password("secret")
    login_page.show_password()
    login_page.expect_password_visible()
    login_page.hide_password()
    login_page.expect_password_hidden()
    login_page.expect_show_button_visible()


@pytest.mark.login
@pytest.mark.positive
def test_login_pos_004_authenticated_user_redirected_from_login_page(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    login_page.login_with_valid_credentials()
    contacts_page.expect_loaded()
    login_page.open("/login")
    contacts_page.expect_loaded()


@pytest.mark.login
@pytest.mark.negative
def test_login_neg_001_invalid_credentials_display_error(page):
    login_page = LoginPage(page)
    login_page.open_login()
    login_page.login("invalid@example.com", "WrongPassword123!")
    login_page.expect_on_login_page()
    login_page.expect_any_error()


@pytest.mark.login
@pytest.mark.negative
def test_login_neg_002_sign_in_disabled_when_email_is_empty(page):
    login_page = LoginPage(page)
    login_page.open_login()
    login_page.expect_sign_in_disabled()
    login_page.fill_password("password")
    login_page.expect_sign_in_disabled()


@pytest.mark.login
@pytest.mark.negative
def test_login_neg_003_sign_in_disabled_when_password_is_empty(page):
    login_page = LoginPage(page)
    login_page.open_login()
    login_page.fill_email("user@example.com")
    login_page.expect_sign_in_disabled()


@pytest.mark.login
@pytest.mark.negative
def test_login_neg_004_unauthenticated_contacts_access_redirects_to_login(page):
    login_page = LoginPage(page)
    contacts_page = ContactsPage(page)
    contacts_page.open_contacts()
    login_page.expect_on_login_page()
