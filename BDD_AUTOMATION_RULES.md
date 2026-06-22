# BDD & UI Automation Rules

General reference for AI agents and developers. Cursor-specific rule files live in [`.cursor/rules/`](.cursor/rules/).

---

## Workflow (in order)

1. **Understand** frontend and backend code for the target module or feature.
2. **Generate BDD test cases** as an Excel file (see [Automation Testcases Prompt](#automation-testcases-prompt) below).
3. **Implement automation** from that Excel — only positive and negative scenarios — in the project's `tests/` and `pages/` folders.
4. **On frontend or backend changes**, add or update tests and pages for new modules or features without modifying unrelated scenarios.

---

## Automation scope (strict)

| Allowed   | Forbidden                                      |
|-----------|------------------------------------------------|
| `tests/`  | `conftest.py`                                  |
| `pages/`  | Any other file or folder outside `tests/` and `pages/` |

- Do not change existing test scenarios when adding new coverage — isolate new tests and page methods.
- Follow the [UI automation coding rules](#ui-automation-coding-rules) when writing code.

---

## Automation Testcases Prompt

### Context

- Generate automation-ready test cases that will later be converted directly into UI automation scripts.
- Focus only on scenarios suitable for UI automation.

Generate test cases using **STRICT BDD format**.

### Coverage (include only)

1. Positive Scenarios
2. Negative Scenarios
3. Validation
4. Boundary
5. Integration

### Do not generate

- Performance test cases
- Security test cases
- Accessibility test cases
- Compatibility test cases
- Exploratory test cases
- Duplicate scenarios
- Scenarios unsuitable for UI automation

No two rows may cover the same user behavior. Before adding a row, verify the Scenario and Given/When/Then combination is not already present.

### Output requirements

- Generate the output in **Excel format only**.
- **One row per test case.**
- Follow BDD principles strictly.
- Every test case should represent a **single user behavior**.
- Ensure that scenarios are automation-friendly and can be directly converted into Playwright Python.
- Avoid combining multiple assertions into one scenario.

### Excel columns (exact order)

| # | Column                  |
|---|-------------------------|
| 1 | Test Case ID            |
| 2 | Feature                 |
| 3 | Scenario                |
| 4 | Given (Preconditions)   |
| 5 | When (Actions)          |
| 6 | Then (Expected Outcomes)|

### Additional rules

- Test Case IDs must be unique.
- Do not create duplicate test cases — each row must cover a distinct user behavior.
- Scenario names should be concise and descriptive.
- **Given** should contain only initial state.
- **When** should contain only actions.
- **Then** should contain only expected outcomes.
- Generate output as an Excel table only.
- Do not include explanations, notes, assumptions, or summaries.
- Ensure each test case is directly usable for generating UI automation code.
- While creating automation scripts, choose **only stable locators**.

---

## Automation implementation (from Excel)

- Implement **only positive and negative** rows from the Excel file as Playwright tests.
- Do not create duplicate automation tests — review existing `tests/` files before adding; one Excel row maps to one test function.
- Map UI interactions to `pages/` using the Page Object Model.
- Map scenarios to `tests/` with positive and negative markers (e.g. `@pytest.mark.positive`, `@pytest.mark.negative`).
- Define `login_with_valid_credentials()` **once** on `LoginPage` and reuse it in every test that needs authentication — do not duplicate login logic.
- Do not use pytest fixtures for page objects or auth; instantiate page classes manually in tests and call login only when the scenario requires it.
- Use environment variables for credentials and base URLs; never hardcode secrets.
- Choose **only stable locators** — prefer `data-testid`, `#id`, `get_by_role`, and `get_by_placeholder`; avoid brittle XPath and text-based selectors.

---

## UI automation coding rules

When writing or editing tests under `tests/` or `pages/`:

### Architecture

- Use **Page Object Model**: locators and UI actions in `pages/`, scenarios in `tests/`.
- Read the base URL and credentials from environment variables; never hardcode them.
- Keep API details out of page objects — interact with the UI only.

### Locators

Choose **only stable locators**.

1. Prefer `data-testid`, `#id`, `get_by_role`, `get_by_placeholder`, and `get_by_label`.
2. Scope modal and form locators to a container — avoid global XPath.
3. Avoid brittle `contains(text())` XPath selectors and dynamic class names.

### Tests

- Tag every test as positive or negative (e.g. `@pytest.mark.positive`, `@pytest.mark.negative`), plus a module marker when applicable.
- Do not add duplicate test cases — each test must cover a unique scenario; check existing tests in the module first.
- Each module should have at least one positive and one negative scenario.
- Do not use pytest fixtures for page objects or authentication — instantiate `LoginPage`, `ContactsPage`, etc. manually in each test using the `page` argument from `conftest.py`.
- When a scenario requires an authenticated user, call `LoginPage.login_with_valid_credentials()` manually in that test (or once at the start of a test module when sharing session is intentional).
- Generate dynamic test data via a shared utility module when needed.

### Page objects

- Extend a shared base page class for common URL and error helpers.
- Define `login_with_valid_credentials()` **once** on `LoginPage`; all tests that need a valid login must reuse this method — do not duplicate login logic in tests or helpers.
- Methods return `None`; use `expect_*` naming for assertions.
- Put assertions in page objects or dedicated assertion methods, not on raw locators in test files.

### Do not

- Use `time.sleep()` — use Playwright `expect()` or framework-appropriate waits.
- Put assertions directly on raw `page.locator()` in test files.
- Add duplicate test cases that cover the same scenario as an existing test.
- Modify `conftest.py` or files outside `tests/` and `pages/` unless explicitly requested.
