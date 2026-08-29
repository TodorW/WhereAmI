# Changelog

## 2.0.0

Full rewrite from the original single-file script.

### Fixed
- Category bucketing bug that silently dropped ~50 of ~106 sites from every
  scan (a self-referential `locals()` check that could never be true).
- False "account exists" results for sites that were only checked via their
  homepage URL (Netflix, Amazon, PayPal, Coursera, etc.) — those entries are
  removed; homepage-only checks can't distinguish accounts at all.
- Username-style platforms (GitHub, Reddit, Steam, ...) were being queried
  with the raw email address instead of a username, guaranteeing near-100%
  false negatives on those sites.

### Added
- `--username` flag as the primary, accurate way to run checks; `--email`
  still works and derives a username from the local part.
- Per-site `confidence` rating (high/medium/low) surfaced in the output,
  so SPA/bot-protected platforms are labeled instead of silently trusted.
- `not_found_marker` support for sites that return HTTP 200 for missing
  accounts but include distinguishing text (e.g. Steam, Hacker News).
- Concurrent scanning (`--workers`, capped at 20) instead of one-at-a-time.
- `--category` filter and `--only-found` flag.
- JSON/CSV export via `--output` / `--format`.
- Retry with backoff and an HTTPS-only transport on the shared HTTP session.
- Full test suite (pytest), lint (ruff), static security scan (bandit),
  and dependency vulnerability scan (pip-audit), all wired into CI.
- Dependabot for weekly dependency updates.

### Removed
- The unused `method`/`success_codes` parameters that were never actually
  passed by any caller in the old script (now properly used per-site).
