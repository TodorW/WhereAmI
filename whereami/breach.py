"""Optional breach lookup via the Have I Been Pwned API.

The API key is read only from an environment variable, never accepted as a
CLI argument: a CLI flag would land in shell history and in `ps` output for
other local users, while an environment variable set in a non-exported
shell command or a secrets manager does not.
"""

import os
from urllib.parse import quote

import requests

from .http_client import DEFAULT_TIMEOUT_SECONDS, build_session

HIBP_API_KEY_ENV = "HIBP_API_KEY"
_ENDPOINT = "https://haveibeenpwned.com/api/v3/breachedaccount/{email}"


class BreachCheckError(RuntimeError):
    pass


def check_breaches(email: str, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> list[str]:
    api_key = os.environ.get(HIBP_API_KEY_ENV)
    if not api_key:
        raise BreachCheckError(
            f"set the {HIBP_API_KEY_ENV} environment variable to your own "
            "Have I Been Pwned API key to use --check-breach"
        )

    session = build_session()
    url = _ENDPOINT.format(email=quote(email, safe=""))
    headers = {"hibp-api-key": api_key}

    try:
        response = session.get(
            url, headers=headers, params={"truncateResponse": "true"}, timeout=timeout
        )
    except requests.exceptions.RequestException as exc:
        raise BreachCheckError(f"request to Have I Been Pwned failed: {type(exc).__name__}") from exc

    if response.status_code == 404:
        return []
    if response.status_code == 401:
        raise BreachCheckError("Have I Been Pwned rejected the API key (401 Unauthorized)")
    if response.status_code == 429:
        raise BreachCheckError("Have I Been Pwned rate limit hit (429); try again later")
    if response.status_code != 200:
        raise BreachCheckError(f"Have I Been Pwned returned an unexpected status {response.status_code}")

    return [entry["Name"] for entry in response.json()]
