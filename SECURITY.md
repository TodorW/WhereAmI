# Security Policy

## Scope

WhereAmI is a local CLI tool. It makes outbound HTTPS requests to third-party
sites on the user's behalf and does not run a server, store credentials, or
transmit data to any service controlled by this project.

## Reporting a Vulnerability

If you find a security issue (e.g. a way to inject data into a request, an
SSRF vector, or a dependency with a known CVE that isn't caught by CI),
please open a private security advisory on GitHub rather than a public issue:

`Security` tab -> `Report a vulnerability`

Please include:
- A description of the issue and its impact
- Steps to reproduce
- The version/commit affected

## API Keys

The optional `--check-breach` feature (Have I Been Pwned) reads its API key
only from the `HIBP_API_KEY` environment variable. It is never accepted as a
CLI flag, because a flag value ends up in shell history and in `ps` output
visible to other local users; an environment variable set via a secrets
manager or an un-exported shell command does not.

## Supported Versions

Only the latest commit on `main` is supported. There are no long-term
maintenance branches.

## Automated Checks

Every push and pull request runs:
- `bandit` static analysis for common Python security issues
- `pip-audit` against `requirements.txt` for known CVEs in dependencies
- The full test suite

Dependabot opens weekly PRs for outdated dependencies and GitHub Actions.
