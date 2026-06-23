# UI Automation Rules

---

## Definitions

- **Provided BDD file** — The Excel workbook (`.xlsx`) containing BDD test cases for the project. **The filename is not fixed** — use whatever path or name the user, project README, environment variable, or task specifies (e.g. `bdd_cases.xlsx`, `login_regression.xlsx`). Throughout these rules, *provided BDD file* means that supplied workbook — never hardcode a specific filename in rules, automation code, or documentation.

---

## Mandatory: FE/BE change sync (always apply)

When the user asks for **any frontend or backend code change** — new feature, bug fix, UI update, API change, validation change — update automation in the **same task**, without waiting to be asked separately.

**FE/BE code is the source of truth for locators.** The **provided BDD file** is the source of truth for **what** to automate. Locators, page objects, and pytest tests must reflect the **actual** implemented UI/API and the **provided** BDD rows — never assumptions or copy-paste from other modules. See [FE/BE → automation sync flow](#febe--automation-sync-flow-source-of-truth).

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
| **FE / BE** | Implementation | Source of truth for locators — actual markup, labels, roles, routes, validation messages. Every BDD step must map to real UI/API behavior in the code. |
| **Locators** | FE DOM / accessibility tree | Defined only after reading FE/BE **and** the BDD row. Each locator must target a real element using stable attributes the FE exposes. |
| **Page objects** | Locators + BDD When/Then | Actions and assertions implement BDD steps; no raw locators in tests. |
| **Tests** | Provided BDD rows + page objects | One test per BDD row; tests call page methods only. |
| **Execution** | Running application | Required gate before any layer is considered done. |

### Before writing or updating automation

1. **Locate** the provided BDD file for the project (from user, README, or task — filename varies).
2. **Read** the BDD row(s) for the feature — Given, When, Then.
3. **Open and read** the FE component(s), page(s), and related BE handlers for that feature.
4. **Record** actual copy from FE/BE: headings, button labels, placeholders, error messages, routes, modal titles, table columns.
5. **Confirm** each BDD step maps to the implementation and each interactive element is locatable per the [testable form markup](#testable-form-markup-fe--automation-contract) contract.
6. **Then** implement locators → page objects → tests in that order.

### Before writing or updating FE / BE

1. **Check** whether automation already covers the feature (BDD row + page + test in the provided file).
2. **Preserve or update** accessible names, ids, roles, and user-visible messages intentionally — breaking changes require the same-task automation sync.
3. **Do not** merge FE that removes or changes locators without updating automation in the same change.

### Drift prevention (do not)

- Create, edit, or regenerate the provided BDD file (unless the user explicitly requests it).
- Hardcode a specific BDD filename in rules, code, or docs — always use the file supplied for the project.
- Write tests or locators from memory, tickets, or other projects without reading the **provided BDD file** and current FE/BE code.
- Add locators that assume markup the FE does not implement (e.g. label association when `htmlFor`/`id` is missing).
- Copy locators from one module into another without verifying the target FE matches.
- Ship automation in a later PR than the FE/BE it depends on.
- Consider automation complete without executing tests against the live app.

### Failure handling

| Symptom | Action |
|---------|--------|
| Locator not found | Inspect FE markup first; fix FE testable markup or update locator to match reality — never add structural/CSS workarounds without FE fix. |
| Test assertion mismatch | Compare BDD Then clause to actual UI text/behavior in FE; update test/locator or fix FE — keep BDD row, FE, and automation aligned. |
| BDD row does not match FE/BE | **Report the gap** to the user — do not edit the Excel file or invent automation that bypasses the mismatch. |
| New UI, no BDD row in provided file | **Stop** — request an updated BDD file from the provider; do not add rows yourself. |
| BDD file path unknown | Ask the user or check project README / config for the provided BDD file location — do not assume a default filename. |

---

## Workflow (in order)

Follow the [FE/BE → automation sync flow](#febe--automation-sync-flow-source-of-truth). Summary:

1. **Locate and read** the provided BDD file for the target feature (input only — do not edit).
2. **Read** frontend and backend code for that feature (source of truth for locators).
3. **Implement locators** in `pages/locators/` from the current FE DOM / accessibility tree, mapped to BDD When/Then steps.
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

- While creating automation scripts, choose **only stable locators**.
- After implementing any test cases, execute them against the application and resolve any failures encountered. Ensure all test cases pass successfully before considering the implementation complete.
- **FE/BE → automation sync:** Locators, page objects, and tests must be derived from the **provided BDD file** and kept in sync with actual FE/BE code — see [FE/BE → automation sync flow](#febe--automation-sync-flow-source-of-truth). Never author automation from assumptions alone.
- **Testable form markup (FE + automation contract):** See [Testable form markup](#testable-form-markup-fe--automation-contract) below. Applies to every new form, modal, and field — including greenfield projects with no existing reference screens.

---

## Testable form markup (FE + automation contract)

Use this contract whenever **frontend**, **backend-driven UI**, or **automation** touches a form. It is stack- and project-agnostic.

### Principle

A field is **testable** only when tools (automation, assistive tech) can find it by **accessible name** or **stable id** — not by layout, CSS classes, or DOM sibling position.

### Frontend contract (build this from the first form)

For every visible input, select, or textarea:

1. **Expose an accessible name** using one primary method (pick one per field and use it consistently across the app):
   - `<label for="unique-id">` paired with `id="unique-id"` on the control
   - Control nested inside `<label>`
   - `aria-label` on the control
   - `aria-labelledby` pointing at visible label text
   - `data-testid` (or equivalent stable test attribute) when a visible label is not appropriate
2. **Keep the accessible name stable** — use the field’s semantic name (e.g. `Email`, `First name`). Put decorative or optional markers (`*`, `(optional)`, hints) in separate elements so they are **not** part of the name used for locating.
3. **Use unique, predictable ids** — scope by feature if needed (e.g. `signup-email`, `edit-contact-phone`); never rely on auto-generated or positional ids.
4. **Scope containers semantically** — forms, dialogs, and modals should use appropriate roles (`form`, `dialog`) or a stable wrapper id / `data-testid` so locators stay local to that surface.
5. **Apply the same pattern everywhere** — every form in the project follows the same association approach; do not mix labelled and unlabelled fields.

### Automation contract

1. **Locate fields the way users do** — prefer, in order: role + accessible name, label, stable `#id`, placeholder (only when fixed), then explicit `data-testid`.
2. **Scope first** — resolve locators inside the form, dialog, or page section container; avoid page-global queries when a container exists.
3. **Fix markup before workarounds** — if a label-based or id-based locator fails, treat it as an FE defect. Do **not** compensate with CSS utility classes, text-proximity filters, nth-child, or structural XPath.
4. **Verify before merge** — for each new or changed field, confirm the chosen locator resolves exactly one target control (e.g. Playwright `get_by_label` / accessibility tree, browser devtools, or project inspector). FE and automation changes for the same form ship together only after every field passes this check.

### Do not

- Ship visually labelled fields without a programmatic label link.
- Embed required `*` or helper text inside the accessible name used for automation.
- Add automation-only locators that depend on styling hooks (`space-y-1`, grid order, etc.).
- Merge locator PRs when the underlying field is not resolvable by the agreed strategy.

---

## Automation implementation (from provided BDD)

- Implement **only positive and negative** rows from the **provided** BDD file as Playwright tests.
- Do not create duplicate automation tests — review existing `tests/` files before adding; one BDD row maps to one test function.
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
- **Provided BDD + FE/BE in sync** — read the provided BDD file and FE/BE implementation before writing locators or tests; keep all layers aligned per [FE/BE → automation sync flow](#febe--automation-sync-flow-source-of-truth).

### Locators

Choose **only stable locators**.

1. Prefer `data-testid`, `#id`, `get_by_role`, `get_by_placeholder`, and `get_by_label`.
2. Scope modal and form locators to a container — avoid global XPath.
3. Avoid brittle `contains(text())` XPath selectors and dynamic class names.
4. Follow the [Testable form markup](#testable-form-markup-fe--automation-contract) contract — fix FE accessible names before adding structural or CSS-based locator workarounds.

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
- Create, edit, or regenerate the provided BDD file unless the user explicitly asks.
- Hardcode a specific BDD filename — use the file path supplied for the project.
