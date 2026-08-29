<div align="center">

# WhereAmI

**Find out which sites still have a profile tied to your username or email.**

[![CI](https://github.com/TodorW/WhereAmI/actions/workflows/ci.yml/badge.svg)](https://github.com/TodorW/WhereAmI/actions/workflows/ci.yml)
[![Security](https://github.com/TodorW/WhereAmI/actions/workflows/security.yml/badge.svg)](https://github.com/TodorW/WhereAmI/actions/workflows/security.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

WhereAmI is a Python CLI for personal digital-footprint audits. Give it a
username (or an email — it derives the local part) and it checks 45
real, individually-verified sites, tells you where a profile likely exists,
and how much you should trust that answer.

It exists because most "check 100 sites" scripts either check homepage URLs
that always return the same thing (worthless), or key everything off a raw
email address on sites that only key profiles by username (worthless in a
different way). WhereAmI's entire design is built around avoiding both.

> **Responsible use only.** This tool is for auditing your own digital
> footprint or for authorized security research. Do not use it to look up
> someone else's accounts without their consent, harass anyone, or violate
> a target site's terms of service.

## Table of Contents

- [Why this exists](#why-this-exists)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration file](#configuration-file)
- [Breach checking](#breach-checking)
- [Comparing scans over time](#comparing-scans-over-time)
- [Shell completion](#shell-completion)
- [Architecture](#architecture)
- [Confidence ratings](#confidence-ratings)
- [Categories](#categories)
- [Privacy & security](#privacy--security)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Why this exists

The previous version of this tool had two bugs that made most of its
"100+ sites" claim meaningless: a category-bucketing bug silently dropped
about half the site list from every run, and roughly a dozen entries were
homepage URLs that return HTTP 200 for literally anyone, guaranteeing a
false "account exists" every time. See [CHANGELOG.md](CHANGELOG.md) for the
full list of what was fixed and added in the rewrite.

## Installation

```bash
git clone https://github.com/TodorW/WhereAmI.git
cd WhereAmI
pip install -r requirements.txt
```

Requires Python 3.11+. To install it as a proper command (`whereami` on your
`PATH`) instead of running the script directly:

```bash
pip install .
```

## Usage

```bash
# by username — recommended, since most sites key profiles by username
whereami --username your_handle

# by email — the part before the @ is used as the username
whereami --email you@example.com

# no flags: prompts interactively
whereami

# filter to one or more categories
whereami --username your_handle --category Development --category Gaming

# only show hits, write full results to a file
whereami --username your_handle --only-found --output results.json

# list available categories
whereami --list-categories
```

Also runnable as `python whereami.py`, `python -m whereami`, or, once
installed, as `whereami`.

<details>
<summary>All flags</summary>

| Flag | Description |
|---|---|
| `--username NAME` | Username to check across sites |
| `--email ADDRESS` | Email address; the local part is used as the username |
| `--category NAME` | Limit the scan to one category (repeatable) |
| `--only-found` | Only print sites where an account was found |
| `--workers N` | Concurrent requests (default 8, max 20) |
| `--timeout N` | Per-request timeout in seconds (default 8) |
| `--host-concurrency N` | Max simultaneous requests to the same host (default 2) |
| `--diff PATH` | Compare against a previous `--output json` export |
| `--check-breach` | Check `--email` against Have I Been Pwned (needs `HIBP_API_KEY`) |
| `--output PATH` | Write results to a file, or `-` for stdout |
| `--format {json,csv}` | Export format for `--output` |
| `--no-color` | Disable colored output |
| `--quiet` | Suppress progress/summary text (only `--output` prints) |
| `--config PATH` | Path to a config file (default: `~/.whereami.toml`) |
| `--list-categories` | List available categories and exit |
| `--version` | Print the version and exit |

</details>

### Example output

```
Checking 'your_handle' against 45 sites...

✓ GitHub (high confidence) - status 200
✗ Reddit - status 404
? Facebook - status 302

--- Summary ---
Found:     6
Not found: 30
Uncertain: 8
Errors:    1
```

### Scripting / piping

```bash
whereami --username your_handle --quiet --output - --format json | jq '.[] | select(.verdict=="found")'
```

## Configuration file

Recurring flags can live in `~/.whereami.toml` (or any path passed via
`--config`); CLI flags always override it. See
[whereami.example.toml](whereami.example.toml):

```toml
workers = 8
timeout = 8
host_concurrency = 2
only_found = false
no_color = false
format = "json"
categories = ["Development", "Gaming"]
```

## Breach checking

`--check-breach` looks up `--email` against
[Have I Been Pwned](https://haveibeenpwned.com/), which requires your own
API key:

```bash
export HIBP_API_KEY=your-own-key
whereami --email you@example.com --check-breach
```

The key is read **only** from the `HIBP_API_KEY` environment variable —
never accepted as a CLI flag — so it can't end up in your shell history or
in `ps` output for other users on the same machine. See
[SECURITY.md](SECURITY.md).

## Comparing scans over time

Save a scan, then diff a later one against it to see what changed:

```bash
whereami --username your_handle --output first-scan.json
# ... weeks later ...
whereami --username your_handle --diff first-scan.json
```

```
--- Changes since last scan ---
New: Mastodon
Lost: Vine
```

## Shell completion

```bash
source completions/whereami.bash   # or add this line to ~/.bashrc
```

## Architecture

| Module | Responsibility |
|---|---|
| `whereami/sites.py` | The site database: name, category, URL template, confidence |
| `whereami/checker.py` | Single-site check: build URL, request, interpret into a `Verdict` |
| `whereami/concurrency.py` | Runs checks concurrently, capped globally and per-host |
| `whereami/http_client.py` | Shared `requests.Session`: retry/backoff, HTTPS-only transport |
| `whereami/history.py` | Diffing a scan against a previous JSON export |
| `whereami/breach.py` | Optional Have I Been Pwned lookup |
| `whereami/config.py` | Loads `~/.whereami.toml` |
| `whereami/report.py` / `whereami/export.py` | Console rendering, JSON/CSV export |
| `whereami/cli.py` | Argument parsing and orchestration |

## Confidence ratings

Every site carries an honest `confidence` label instead of pretending
uniform accuracy:

| Rating | Meaning |
|---|---|
| `high` | JSON/API-backed, or a page with a reliably correct 404 |
| `medium` | Server-rendered page, generally reliable, occasionally flaky |
| `low` | Client-rendered (SPA) or bot-protected — often returns 200 regardless of whether the account exists |

A `low`-confidence hit is a lead worth checking manually by hand, never
proof. Some sites (Steam, Hacker News, Twitch) return 200 either way but
include distinguishing text, so they're checked with a verified
`not_found_marker` instead of trusting the status code alone — see
[CONTRIBUTING.md](CONTRIBUTING.md) for how to add more of these.

## Categories

Social Media, Professional, Video & Streaming, Music, Gaming, Photo,
Development, Design, Productivity, Community & Forums, Fitness, Funding &
Crowdsourcing. Run `--list-categories` for the exact, current list.

## Privacy & security

- Nothing is written to disk unless you pass `--output`.
- All checks run locally, directly from your machine to the target site —
  no data passes through any server this project controls.
- The HTTP session cannot make plaintext `http://` requests; the adapter is
  removed entirely, not just unused.
- Every request has a timeout, with a small bounded retry for transient
  failures — no request can hang indefinitely.
- The `HIBP_API_KEY` for `--check-breach` is read from the environment only,
  never a CLI flag (see [Breach checking](#breach-checking)).
- CI runs `bandit` (static security analysis) and `pip-audit` (dependency
  CVE scanning) on every change, plus a weekly scheduled security scan.
  Dependabot opens PRs for outdated dependencies automatically. Full policy
  in [SECURITY.md](SECURITY.md).

## Limitations

- `low`-confidence sites often return 200 regardless of whether the account
  exists (SPA rendering, anti-bot pages) — treat those as leads, not facts.
- Sites with aggressive bot protection (Cloudflare challenges, etc.) may
  block automated requests entirely, showing up as errors or timeouts.
- Results are indicative, not definitive, even for `high`-confidence sites.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup, the required
checks, and how to add a new site to the database.

## License

MIT — see [LICENSE](LICENSE).

---

**Use WhereAmI on your own accounts to improve your digital hygiene, not to
look someone else up without their consent.**
