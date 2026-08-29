from unittest.mock import MagicMock

import requests

from whereami.checker import Verdict, check_site
from whereami.sites import Category, Confidence, Site

SITE = Site("Example", Category.SOCIAL, "https://example.com/{value}", Confidence.MEDIUM)


def _session_returning(status_code, text=""):
    session = MagicMock()
    response = MagicMock()
    response.status_code = status_code
    response.text = text
    session.get.return_value = response
    return session


def test_found_on_success_code():
    session = _session_returning(200)
    result = check_site(session, SITE, "someone")
    assert result.verdict == Verdict.FOUND


def test_not_found_on_404():
    session = _session_returning(404)
    result = check_site(session, SITE, "someone")
    assert result.verdict == Verdict.NOT_FOUND


def test_uncertain_on_other_status():
    session = _session_returning(302)
    result = check_site(session, SITE, "someone")
    assert result.verdict == Verdict.UNCERTAIN


def test_not_found_marker_overrides_status_code():
    site = Site(
        "Marked",
        Category.SOCIAL,
        "https://example.com/{value}",
        Confidence.MEDIUM,
        not_found_marker="could not be found",
    )
    session = _session_returning(200, text="Sorry, this profile could not be found")
    result = check_site(session, site, "someone")
    assert result.verdict == Verdict.NOT_FOUND


def test_timeout_becomes_error_verdict():
    session = MagicMock()
    session.get.side_effect = requests.exceptions.Timeout()
    result = check_site(session, SITE, "someone")
    assert result.verdict == Verdict.ERROR
    assert "timed out" in result.detail


def test_connection_error_becomes_error_verdict():
    session = MagicMock()
    session.get.side_effect = requests.exceptions.ConnectionError()
    result = check_site(session, SITE, "someone")
    assert result.verdict == Verdict.ERROR


def test_username_is_url_encoded():
    session = _session_returning(200)
    check_site(session, SITE, "weird value/with?chars")
    called_url = session.get.call_args[0][0]
    assert " " not in called_url
    assert "/with?" not in called_url


def test_head_method_is_used_when_configured():
    site = Site("HeadSite", Category.SOCIAL, "https://example.com/{value}", Confidence.MEDIUM, method="head")
    session = _session_returning(200)
    check_site(session, site, "someone")
    session.head.assert_called_once()
    session.get.assert_not_called()
