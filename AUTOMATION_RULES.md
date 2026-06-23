# UI Automation Rules

---

## Definitions

- **Provided BDD file** — The Excel workbook (`.xlsx`) containing BDD test cases for the project. **The filename is not fixed** — use whatever path or name the user, project README, environment variable, or task specifies (e.g. `bdd_cases.xlsx`, `login_regression.xlsx`). Throughout these rules, *provided BDD file* means that supplied workbook — never hardcode a specific filename in rules, automation code, or documentation.

---

## Mandatory: FE/BE change sync (always apply)

When the user asks for **any frontend or backend code change** — new feature, bug fix, UI update, API change, validation change — update automation in the **same task**, without waiting to be asked separately.

**FE/BE code is the source of truth for functionality and user-visible behavior. Automation owns the locator strategy. Locators must be derived from the current DOM structure and implemented using stable, semantic, relative XPath expressions scoped to stable containers.**

**Do not create, edit, or regenerate** the provided BDD file — it is supplied externally. If a BDD row does not match the current FE/BE, report the gap; do not modify the Excel file unless the user explicitly asks.

**Required order after the app code change:**

1. **Read** the modified FE/BE files — routes, components, labels, roles, validation messages, API responses.
2. **Read** the provided BDD file — identify affected rows for the changed feature (do not edit the file).
3. **Update** `pages/` locators — map each BDD When/Then step to elements that exist in the current FE markup (stable locators only; verify each resolves).
4. **Update** `pages/` actions and `tests/` — implement the affected BDD rows using those locators; one BDD row → one test function.
5. **Run** affected tests against the running app; fix FE or automation until all pass.
6. **Leave unchanged** — unrelated modules, unrelated BDD rows, and unrelated test scenarios.

**Do not** consider the FE/BE task complete until steps 3–5 are done for every user-visible behavior covered by the provided BDD rows for that feature.

If the change has **no UI impact** (e.g. internal refactor only), state that briefly and skip automation updates.

---

## FE/BE → automation sync flow (source of truth)

Use this flow for **every** feature — new or existing, greenfield or mature — to prevent drift between application code and automation.

### Sync chain (always in this order)

```
Provided BDD file (Excel)  ──┐
                             ├──→  Locators  →  Page objects  →  Tests  →  Execute & pass
FE / BE code  ───────────────┘              ↑___________________________________|
                                                  (failures loop back to FE/BE or automation)
```

| Layer | Source | Rule |
|-------|--------|------|
| **BDD test cases** | **Provided BDD file** (read-only; any `.xlsx` filename) | Defines scenarios to automate. **Do not generate or update this file.** Implement only rows that exist in the provided file. |
| FE / BE | Implementation | Source of truth for functionality, validation, routes, labels, and user-visible behavior. Automation owns locator strategy. |
| **Locators** | FE DOM + [Locator strategy rules](#locator-strategy-rules) | Scoped relative XPath only, derived after reading FE/BE and the BDD row. Each expression must resolve a real element in the current markup. |
| **Page objects** | Locators + BDD When/Then | Actions and assertions implement BDD steps; no raw locators in tests. |
| **Tests** | Provided BDD rows + page objects | One test per BDD row; tests call page methods only. |
| **Execution** | Running application | Required gate before any layer is considered done. |

### Before writing or updating automation

1. **Locate** the provided BDD file for the project (from user, README, or task — filename varies).
2. **Read** the BDD row(s) for the feature — Given, When, Then.
3. **Open and read** the FE component(s), page(s), and related BE handlers for that feature.
4. **Record** actual copy from FE/BE: headings, button labels, placeholders, error messages, routes, modal titles, table columns.
5. Confirm each BDD step maps to the implementation and each interactive element can be targeted with stable, semantic, relative XPath expressions according to the locator strategy rules.
6. **Then** implement locators → page objects → tests in that order.

### Before writing or updating FE / BE

1. **Check** whether automation already covers the feature (BDD row + page + test in the provided file).
2. **Preserve or update** accessible names, ids, roles, and user-visible messages intentionally — breaking changes require the same-task automation sync.
3. **Do not** merge FE that removes or changes locators without updating automation in the same change.

### Drift prevention (do not)

- Create, edit, or regenerate the provided BDD file (unless the user explicitly requests it).
- Hardcode a specific BDD filename in rules, code, or docs — always use the file supplied for the project.
- Write tests or locators from memory, tickets, or other projects without reading the **provided BDD file** and current FE/BE code.
- Create XPath expressions based on assumptions instead of inspecting the current DOM structure.
- Copy locators from one module into another without verifying the target FE matches.
- Ship automation in a later PR than the FE/BE it depends on.
- Consider automation complete without executing tests against the live app.

### Failure handling

| Symptom | Action |
|---------|--------|
| Locator not found | Inspect FE markup first and update scoped relative XPath to match the current DOM structure. Prefer container-first design and reusable dynamic form locators. Never switch to CSS selectors, Playwright get_by_* APIs, positional indexes, or absolute XPath. |
| Test assertion mismatch | Compare the BDD Then clause with the current application behavior and update page objects, assertions, or locators as necessary while keeping the BDD scenario aligned. |
| BDD row does not match FE/BE | **Report the gap** to the user — do not edit the Excel file or invent automation that bypasses the mismatch. |
| New UI, no BDD row in provided file | **Stop** — request an updated BDD file from the provider; do not add rows yourself. |
| BDD file path unknown | Ask the user or check project README / config for the provided BDD file location — do not assume a default filename. |

---

## Workflow (in order)

Follow the [FE/BE → automation sync flow](#febe--automation-sync-flow-source-of-truth). Summary:

1. **Locate and read** the provided BDD file for the target feature (input only — do not edit).
2. Read frontend and backend code for that feature (source of truth for functionality and user-visible behavior).
3. **Implement locators** in `pages/locators/` as scoped relative XPath from the current FE DOM, mapped to BDD When/Then steps.
4. **Implement or update** page actions and pytest tests from the provided BDD rows — only positive and negative scenarios as defined in the file.
5. **Execute** tests against the running app; loop back to FE/BE or automation until all pass.
6. **On every subsequent FE/BE change**, repeat for affected BDD rows in the provided file only.

---

## Automation scope (strict)

| Allowed | Forbidden |
|---------|-----------|
| `tests/` | `conftest.py` |
| `pages/` | Provided BDD file (Excel — read-only; filename varies by project; do not create or edit) |
| | Any other file or folder outside the allowed list |

- Do not change existing test scenarios when adding new coverage — isolate new tests and page methods.
- Follow the [UI automation coding rules](#ui-automation-coding-rules) when writing code.

---

## BDD test cases file (provided input — read only)

The **provided BDD file** is supplied externally (any `.xlsx` filename). Automation is generated **from** this file; the file itself is **out of scope** for creation or updates.

### How to use the provided file

- **Locate** the file path from the user, project README, or task context.
- **Read** rows for the target feature before writing locators, page objects, or tests.
- Implement **only** scenarios present in the file (typically positive and negative rows).
- Map **one BDD row → one test function**; use the Test Case ID in the test name where applicable.
- Align each Given/When/Then step with real FE/BE behavior — if a step cannot be mapped, report it; do not alter the Excel file.

### Expected column format (for reading)

| # | Column |
|---|--------|
| 1 | Test Case ID |
| 2 | Feature |
| 3 | Scenario |
| 4 | Given (Preconditions) |
| 5 | When (Actions) |
| 6 | Then (Expected Outcomes) |

### Additional rules (automation from provided BDD)

- While creating automation scripts, use **XPath exclusively** per [Locator strategy rules](#locator-strategy-rules).
- After implementing any test cases, execute them against the application and resolve any failures encountered. Ensure all test cases pass successfully before considering the implementation complete.
- **FE/BE → automation sync:** Locators, page objects, and tests must be derived from the **provided BDD file** and kept in sync with actual FE/BE code — see [FE/BE → automation sync flow](#febe--automation-sync-flow-source-of-truth). Never author automation from assumptions alone.

---

## Automation implementation (from provided BDD)

- Implement **only positive and negative** rows from the **provided** BDD file as Playwright tests.
- Do not create duplicate automation tests — review existing `tests/` files before adding; one BDD row maps to one test function.
- Map UI interactions to `pages/` using the Page Object Model.
- Map scenarios to `tests/` with positive and negative markers (e.g. `@pytest.mark.positive`, `@pytest.mark.negative`).
- Define `login_with_valid_credentials()` **once** on `LoginPage` and reuse it in every test that needs authentication — do not duplicate login logic.
- Do not use pytest fixtures for page objects or auth; instantiate page classes manually in tests and call login only when the scenario requires it.
- Use environment variables for credentials and base URLs; never hardcode secrets.
- Use **XPath exclusively** for all UI locators — see [Locator strategy rules](#locator-strategy-rules).

---

## Locator strategy rules

XPath is the only permitted locator type in this framework.

Automation owns locator strategy. Frontend and backend define functionality, but locator implementation belongs to automation.

### Generic form strategy

Repeated forms and modals must use reusable dynamic locator builders rather than hardcoded field locators.

Example:

```python
def input_by_label(container, label):
    return container.locator(
        f'xpath=.//label[contains(normalize-space(),"{label}")]/parent::div/input'
    )
```
### Required

- Use XPath exclusively for all UI locators.
- Create stable, semantic, relative XPath expressions.
- Scope every XPath to the nearest stable container (form, modal, section, table, drawer, tab, etc.).
- Never use page-global XPath when a stable container exists.
- Separate container locators from child locators.
- Reuse container locators throughout the module.
- Prefer parent-child relationships over positional indexes.
- Prefer ancestor-descendant and sibling relationships over deep DOM traversal.
- Use normalize-space() when matching visible text.
- Keep XPath expressions readable and maintainable.
- Store locators in page-specific locator files.
- Reuse existing locators whenever possible.
- Modify locators only when required for stability or UI changes.
- Prefer reusable locator builders over module-specific field locators whenever a common pattern exists.

Use:

```python
self.first_name_input = input_by_label(self.modal, "First name")
```

### Container strategy

Always separate container locators from child locators.

Example:

```python
CONTACT_MODAL =
'//h2[normalize-space()="Add Contact"]/ancestor::div[contains(@class,"rounded-lg")]'
```

Then:

```python
FIRST_NAME =
'.//label[contains(normalize-space(),"First name")]/parent::div/input'
```

Use:

```python
self.modal = page.locator(f"xpath={CONTACT_MODAL}")
self.first_name_input = self.modal.locator(f"xpath={FIRST_NAME}")
```

### Validation rule

Before finalizing a locator, verify that it resolves to the intended element and remains stable during execution. Validation may use count(), visibility checks, or assertions depending on the scenario.

### Avoid

- Absolute XPath.
- CSS selectors.
- get_by_role().
- get_by_label().
- get_by_text().
- nth().
- Positional indexes.
- Dynamic CSS classes.
- Generated IDs.
- Page-global XPath.
- Deep DOM hierarchies.

## Container-first design

Page objects should separate containers from elements.

Example:

```python
CONTACT_MODAL
CONTACT_TABLE
CONTACT_FORM
```

Elements must be located relative to their parent container.

Avoid long page-global XPath expressions.

Prefer:

```python
self.modal.locator(FIRST_NAME)
```

instead of:

```python
page.locator("//h2[...]//label[...]")
```

This improves maintainability and prevents collisions when the application grows.

## Shared locator utilities

Common patterns must be centralized and reused across modules.

Examples:

```python
input_by_label(container, label)
button_by_text(container, text)
dropdown_by_label(container, label)
checkbox_by_label(container, label)
table_cell(container, text)
error_message(container, text)
```

Avoid recreating identical XPath patterns inside individual page locator files.

New modules must reuse shared locator utilities whenever possible.

## UI automation coding rules

When writing or editing tests under `tests/` or `pages/`:

### Architecture

- Use **Page Object Model**: locators and UI actions in `pages/`, scenarios in `tests/`.
- Read the base URL and credentials from environment variables; never hardcode them.
- Keep API details out of page objects — interact with the UI only.
- **Provided BDD + FE/BE in sync** — read the provided BDD file and FE/BE implementation before writing locators or tests; keep all layers aligned per [FE/BE → automation sync flow](#febe--automation-sync-flow-source-of-truth).

### Locators

Follow [Locator strategy rules](#locator-strategy-rules) — **XPath exclusively**.

1. Use scoped relative XPath anchored on business labels, visible text, and stable containers.
2. Define all XPath in `pages/locators/`; access only through page objects.
3. Verify each XPath resolves exactly one element in the live UI before merge.
4. Keep locators aligned with the current DOM structure and business-visible text to maintain stability.

### Locator file rules

- One locator file per page/module under `pages/locators/`.
- Reuse existing XPath definitions before adding new ones.
- Modify locators only when required for stability or UI changes.
- Keep test files free of locator strings — interact through page objects only.
- Ensure locator changes stay scoped and do not break unrelated scenarios.

### Tests

- Tag every test as positive or negative (e.g. `@pytest.mark.positive`, `@pytest.mark.negative`), plus a module marker when applicable.
- Do not add duplicate test cases — each test must cover a unique scenario; check existing tests in the module first.
- Each module should have at least one positive and one negative scenario.
- Do not use pytest fixtures for page objects or authentication — instantiate `LoginPage`, `ContactsPage`, etc. manually in each test using the `page` argument from `conftest.py`.
- When a scenario requires an authenticated user, call `LoginPage.login_with_valid_credentials()` manually in that test (or once at the start of a test module when sharing session is intentional).
- Generate dynamic test data via a shared utility module when needed.
- After creating or updating tests, execute them against the running application and fix all failures before considering the implementation complete.
- Test implementation is not complete until all affected scenarios pass successfully.

### Page objects

- Extend a shared base page class for common URL and error helpers.
- Define `login_with_valid_credentials()` **once** on `LoginPage`; all tests that need a valid login must reuse this method — do not duplicate login logic in tests or helpers.
- Methods return `None`; use `expect_*` naming for assertions.
- Put assertions in page objects or dedicated assertion methods, not on raw locators in test files.
- Put XPath only in `pages/locators/` — never in `tests/`.

### Do not

- Use `time.sleep()` — use Playwright `expect()` or framework-appropriate waits.
- Put assertions directly on raw `page.locator()` in test files.
- Use non-XPath locators (`get_by_role`, `get_by_label`, `#id`, CSS selectors) in `pages/locators/` or tests.
- Add duplicate test cases that cover the same scenario as an existing test.
- Modify `conftest.py` or files outside `tests/` and `pages/` unless explicitly requested.
- Create, edit, or regenerate the provided BDD file unless the user explicitly asks.
- Hardcode a specific BDD filename — use the file path supplied for the project.
- Do not hardcode complete page-level XPath expressions repeatedly.
- Do not duplicate field locators across modules.
- Do not define the same XPath in multiple files.
- Do not locate child elements directly from page when a stable container exists.
- Do not create separate locators for identical form patterns; use shared locator builder methods.
- Do not use waits or sleeps to compensate for unstable locators.