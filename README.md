# Makanify Demo — UI Automation

Playwright + pytest automation for the [Makanify demo frontend](https://github.com/ashaymoweb/makanify-demo).

## Prerequisites

- Python 3.12+
- Demo app running at `http://localhost:3000`
- Valid API credentials (`TEST_EMAIL`, `TEST_PASSWORD`)

## Setup

```bash
cp .env.example .env
# Edit .env with your credentials

pip install -r requirements.txt
python -m playwright install chromium
```

## Run tests

```bash
python -m pytest tests/ -m positive
python -m pytest tests/ -m negative
python -m pytest tests/
```

## BDD rules & test cases

See the [makanify-demo-docs](https://github.com/ashaymoweb/makanify-demo-docs) repo for:

- `BDD_AUTOMATION_RULES.md`
- `makanify_bdd_test_cases.xlsx`

## Structure

```
pages/          # Page Object Model
tests/          # Pytest scenarios (positive / negative)
utilities/      # Test data helpers
conftest.py     # Playwright browser fixture (do not duplicate login logic in fixtures)
```

## Conventions

- `login_with_valid_credentials()` is defined **once** on `LoginPage` and reused in tests.
- No pytest fixtures for page objects or auth — instantiate pages manually in each test.
