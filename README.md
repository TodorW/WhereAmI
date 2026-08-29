# 🔍 WhereAmI - Digital Footprint Analyzer

*"Because sometimes you forget where you've been on the internet"*

## 📖 Overview

**WhereAmI** is a Python CLI that checks whether a username (or the local
part of an email address) has a public profile across ~45 real, verifiable
sites — GitHub, Reddit, PyPI, Steam, and more. It's built for personal
digital-footprint audits and OSINT education.

## ⚠️ Disclaimer

**THIS TOOL IS FOR EDUCATIONAL AND PERSONAL SECURITY AUDITING PURPOSES ONLY**

- ✅ **Allowed**: Checking your own accounts
- ✅ **Allowed**: Security research with proper authorization
- ✅ **Allowed**: Learning about web requests and OSINT methodology
- ❌ **Not Allowed**: Checking others' identities without permission
- ❌ **Not Allowed**: Malicious or harassing activities
- ❌ **Not Allowed**: Violating websites' terms of service

By using this tool, you agree to use it responsibly and legally.

## 📦 Installation

```bash
git clone https://github.com/TodorW/WhereAmI.git
cd WhereAmI
pip install -r requirements.txt
```

Requires Python 3.10+.

## 🎯 Usage

```bash
# by username (recommended — most sites key profiles by username, not email)
python whereami.py --username your_handle

# by email (uses the part before the @ as the username)
python whereami.py --email you@example.com

# no flags: prompts interactively
python whereami.py

# filter to one or more categories
python whereami.py --username your_handle --category Development --category Gaming

# only show hits, write full results to a file
python whereami.py --username your_handle --only-found --output results.json

# list available categories
python whereami.py --list-categories
```

Also runnable as `python -m whereami` or, once installed, as `whereami`.

### Example Output

```
Checking 'your_handle' against 46 sites...

✓ GitHub (high confidence) - status 200
✗ Reddit - status 404
? Facebook - status 302

--- Summary ---
Found:     6
Not found: 30
Uncertain: 8
Errors:    2
```

## 🏗️ Architecture

- `whereami/sites.py` — the site database: name, category, URL template,
  and an honest `confidence` rating per site.
- `whereami/checker.py` — single-site check: builds the URL, makes the
  request, interprets the response into a `Verdict`.
- `whereami/concurrency.py` — runs checks concurrently (worker count
  capped at 20 to avoid hammering targets).
- `whereami/http_client.py` — shared `requests.Session` with retry/backoff
  and an HTTPS-only transport (the `http://` adapter is removed entirely).
- `whereami/report.py` / `whereami/export.py` — console output and
  JSON/CSV export.
- `whereami/cli.py` — argument parsing and orchestration.

### Why `confidence` matters

Some platforms (GitHub, PyPI, Reddit's JSON API) reliably return 404 for a
missing account — those are `high` confidence. Others are client-rendered
single-page apps or sit behind bot protection and tend to return `200` for
almost anything (Instagram, TikTok, Twitter/X) — those are marked `low`.
A `low`-confidence hit is a lead worth checking manually, not proof.

## 📋 Supported Categories

Social Media, Professional, Video & Streaming, Music, Gaming, Photo,
Development, Design, Productivity, Community & Forums, Fitness, Funding &
Crowdsourcing. Run `--list-categories` for the exact list.

## 🛡️ Privacy & Security

- Nothing is written to disk unless you pass `--output`.
- All checks happen locally, directly from your machine to the target site.
- The HTTP session cannot make plaintext `http://` requests — only `https://`.
- Every request has a timeout; a limited retry with backoff handles
  transient failures without hanging indefinitely.
- CI runs `bandit` (static security analysis) and `pip-audit` (dependency
  CVE scanning) on every change — see [SECURITY.md](SECURITY.md).

## 🚨 Limitations & Accuracy

- Sites marked `low` confidence often return 200 regardless of whether the
  account exists (SPA rendering, anti-bot pages) — treat those as leads.
- Sites with aggressive bot protection may block automated requests
  entirely, showing as timeouts or connection errors.
- Results are indicative, not definitive, even for `high` confidence sites.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, local checks, and how to
add a new site to the database.

## 📝 License

MIT License - see [LICENSE](LICENSE).

---

**Remember**: use WhereAmI to improve your own digital hygiene, not to
invade someone else's privacy.
