"""Core single-site check logic."""

from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import quote

import requests

from .http_client import DEFAULT_TIMEOUT_SECONDS
from .sites import Site


class Verdict(StrEnum):
    FOUND = "found"
    NOT_FOUND = "not_found"
    UNCERTAIN = "uncertain"
    ERROR = "error"


@dataclass(frozen=True)
class CheckResult:
    site: Site
    verdict: Verdict
    detail: str
    url: str


def check_site(
    session: requests.Session,
    site: Site,
    value: str,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> CheckResult:
    url = site.url_template.format(value=quote(value, safe=""))

    try:
        request = session.head if site.method == "head" else session.get
        response = request(url, timeout=timeout, allow_redirects=False)
    except requests.exceptions.Timeout:
        return CheckResult(site, Verdict.ERROR, "request timed out", url)
    except requests.exceptions.ConnectionError:
        return CheckResult(site, Verdict.ERROR, "connection failed", url)
    except requests.exceptions.RequestException as exc:
        return CheckResult(site, Verdict.ERROR, f"request failed: {type(exc).__name__}", url)

    if site.not_found_marker and site.not_found_marker in response.text:
        return CheckResult(
            site, Verdict.NOT_FOUND, f"status {response.status_code}, not-found marker matched", url
        )

    if response.status_code in site.success_codes:
        return CheckResult(site, Verdict.FOUND, f"status {response.status_code}", url)

    if response.status_code in site.not_found_codes:
        return CheckResult(site, Verdict.NOT_FOUND, f"status {response.status_code}", url)

    return CheckResult(site, Verdict.UNCERTAIN, f"status {response.status_code}", url)
