# Changelog

## 2.1.0

### Added
- Per-host concurrency limiting (`--host-concurrency`, default 2) so a scan
  can't hammer one target even at a high overall `--workers` count.
- `--diff PREVIOUS_JSON` to compare a scan against an earlier JSON export
  and report which sites newly appeared or disappeared as "found".
- Config file support: `~/.whereami.toml` (or `--config PATH`) for default
  `workers`, `timeout`, `host_concurrency`, `categories`, `only_found`,
  `no_color`, and `format`; CLI flags always take precedence. See
  `whereami.example.toml`.
- `--check-breach` — optional Have I Been Pwned lookup for `--email`. The
  API key is read only from the `HIBP_API_KEY` environment variable, never
  a CLI flag, so it can't leak into shell history or process listings.
- `--quiet` and `--output -` (stdout) for scripting/piping into `jq`.
- Colorized summary line in terminal output.
- Bash completion script (`completions/whereami.bash`).

### Changed
- Twitch upgraded from low to medium confidence: verified that the static
  page title stays `Twitch` for missing accounts vs. `{Name} - Twitch` for
  real ones, giving a reliable not-found marker.
- Minimum Python bumped to 3.11 (uses stdlib `tomllib` for config parsing,
  avoiding an extra dependency).

### Removed
- GoFundMe entry: its URL addresses a campaign slug, not a user account, so
  a username there never told you anything real about the account.

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
