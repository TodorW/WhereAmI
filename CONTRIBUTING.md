# Contributing

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Running checks locally

```bash
ruff check .
pytest -q
bandit -r whereami
pip-audit -r requirements.txt
```

All four must pass before opening a pull request; CI runs the same checks.

## Adding a site

1. Add a `Site(...)` entry to `whereami/sites.py` in the right `Category`.
2. The URL must be `https://` and must contain a `{value}` placeholder that
   changes the response when the account exists vs. doesn't.
3. Set `confidence` honestly:
   - `HIGH` for a JSON/API response or a page with a reliable 404.
   - `MEDIUM` for a server-rendered page that's usually reliable.
   - `LOW` for a client-rendered (SPA) or bot-protected page that tends to
     return 200 regardless of whether the account exists.
4. If the site returns 200 for both cases but includes distinguishing text,
   set `not_found_marker` to a substring that only appears when the account
   is absent, instead of marking it `LOW`.
5. Run `pytest tests/test_sites.py` — it enforces https-only URLs, a real
   placeholder, and no duplicate names.

## Style

- No comments explaining *what* code does; only *why*, and only when it's
  non-obvious.
- Keep functions small and single-purpose; this codebase intentionally
  avoids frameworks and heavy abstractions.
