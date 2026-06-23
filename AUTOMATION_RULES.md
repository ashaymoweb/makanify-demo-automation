# UI Automation Rules

---

## Mandatory: FE/BE change sync (always apply)

When the user asks for **any frontend or backend code change** — new feature, bug fix, UI update, API change, validation change — update automation in the **same task**, without waiting to be asked separately.

**Required order after the app code change:**

1. **Understand** what UI behavior changed (read the modified FE/BE files).
2. **Update** `makanify_bdd_test_cases.xlsx` — add, update, or remove rows for the affected feature only (strict BDD columns; no duplicates).
3. **Update** `pages/` — locators and actions for changed UI (stable locators only).
4. **Update** `tests/` — add or adjust positive and negative pytest tests for changed Excel rows only.
5. **Leave unchanged** — unrelated modules, unrelated Excel rows, and unrelated test scenarios.

**Do not** consider the FE/BE task complete until steps 2–4 are done for every user-visible behavior that changed.

If the change has **no UI impact** (e.g. internal refactor only), state that briefly and skip Excel/tests updates.

---

## Workflow (in order)

1. **Understand** frontend and backend code for the target module or feature.
2. **Generate or update BDD test cases** in `makanify_bdd_test_cases.xlsx` (see [Automation Testcases Prompt](#automation-testcases-prompt) below).
3. **Implement or update automation** from that Excel — only positive and negative scenarios — in `tests/` and `pages/`.
4. **On every subsequent frontend or backend change**, repeat: update Excel → update `pages/` → update `tests/` for the affected feature only.

---

## Automation scope (strict)

| Allowed   | Forbidden                                      |
|-----------|------------------------------------------------|
| `tests/`  | `conftest.py`                                  |
| `pages/`  | Any other file or folder outside the allowed list |
| `makanify_bdd_test_cases.xlsx` (add/update rows when FE/BE changes) | |

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
- After implementing any test cases, execute them against the application and resolve any failures encountered. Ensure all test cases pass successfully before considering the implementation complete.

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

### Locator Management Rules

- Maintain separate locator files for each page/module to ensure clear structure and maintainability.
- Use semantic and stable relative XPath locators when application changes cannot be controlled.
- Access locators only through page classes or test step methods; do not hardcode locators inside test cases.
- Centralize all locator definitions so that UI changes require updates in a single location only.
- Prefer business-oriented locators based on labels or stable attributes over indexes, CSS classes, or absolute XPath.
- Modify existing locators only when necessary to improve stability or accommodate UI changes. Avoid unnecessary locator changes.
- Reuse existing locators whenever possible instead of creating duplicate definitions.
- Keep test cases independent of locator implementation details by interacting only through page objects and step methods.
- Avoid using `nth()`, dynamic CSS classes, and absolute XPath unless no stable alternative exists.
- Ensure locator changes are backward-compatible and do not impact unrelated test scenarios.

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
