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

## Automation rules & test cases

Included in this repo:

- `AUTOMATION_RULES.md` — workflow and automation coding rules
- `makanify_bdd_test_cases.xlsx` — BDD test cases (Excel)
- `.cursor/rules/` — agent rules for automation workflow
- `docs/playwright-mcp-setup.md` — Playwright MCP setup
- `playwright-mcp/run-all-tests.js` — optional MCP batch runner

## Structure

```
pages/          # Page Object Model
tests/          # Pytest scenarios (positive / negative)
utilities/      # Test data helpers
conftest.py     # Playwright browser fixture
docs/           # MCP setup guide
```

## Conventions

- `login_with_valid_credentials()` is defined **once** on `LoginPage` and reused in tests.
- No pytest fixtures for page objects or auth — instantiate pages manually in each test.
