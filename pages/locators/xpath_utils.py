from playwright.sync_api import Locator


def input_by_label(container: Locator, label: str) -> Locator:
    return container.locator(
        f'xpath=.//label[contains(normalize-space(),"{label}")]/parent::div//input'
    )


def button_by_text(container: Locator, text: str) -> Locator:
    return container.locator(
        f'xpath=.//button[normalize-space()="{text}"]'
    )


def table_cell(container: Locator, text: str) -> Locator:
    return container.locator(
        f'xpath=.//table//td[normalize-space()="{text}"]'
    )


def table_header(container: Locator, text: str) -> Locator:
    return container.locator(
        f'xpath=.//table//th[normalize-space()="{text}"]'
    )


def error_message(container: Locator, text: str) -> Locator:
    return container.locator(
        f'xpath=.//p[normalize-space()="{text}"]'
    )


def radio_by_label(container: Locator, group_label: str, option_text: str) -> Locator:
    return container.locator(
        f'xpath=.//fieldset[.//legend[contains(normalize-space(),"{group_label}")]]'
        f'//label[contains(normalize-space(),"{option_text}")]//input[@type="radio"]'
    )


def text_element(container: Locator, text: str) -> Locator:
    return container.locator(
        f'xpath=.//*[normalize-space()="{text}"]'
    )
