from unittest.mock import MagicMock, patch

import pytest
import requests

from whereami.breach import BreachCheckError, check_breaches


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("HIBP_API_KEY", raising=False)
    with pytest.raises(BreachCheckError, match="HIBP_API_KEY"):
        check_breaches("someone@example.com")


def _mock_session(status_code, json_data=None):
    session = MagicMock()
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = json_data or []
    session.get.return_value = response
    return session


@patch("whereami.breach.build_session")
def test_404_means_no_breaches(mock_build, monkeypatch):
    monkeypatch.setenv("HIBP_API_KEY", "fake-key")
    mock_build.return_value = _mock_session(404)
    assert check_breaches("someone@example.com") == []


@patch("whereami.breach.build_session")
def test_200_returns_breach_names(mock_build, monkeypatch):
    monkeypatch.setenv("HIBP_API_KEY", "fake-key")
    mock_build.return_value = _mock_session(200, [{"Name": "Adobe"}, {"Name": "LinkedIn"}])
    assert check_breaches("someone@example.com") == ["Adobe", "LinkedIn"]


@patch("whereami.breach.build_session")
def test_401_raises_key_error(mock_build, monkeypatch):
    monkeypatch.setenv("HIBP_API_KEY", "fake-key")
    mock_build.return_value = _mock_session(401)
    with pytest.raises(BreachCheckError, match="401"):
        check_breaches("someone@example.com")


@patch("whereami.breach.build_session")
def test_429_raises_rate_limit_error(mock_build, monkeypatch):
    monkeypatch.setenv("HIBP_API_KEY", "fake-key")
    mock_build.return_value = _mock_session(429)
    with pytest.raises(BreachCheckError, match="rate limit"):
        check_breaches("someone@example.com")


@patch("whereami.breach.build_session")
def test_connection_error_is_wrapped(mock_build, monkeypatch):
    monkeypatch.setenv("HIBP_API_KEY", "fake-key")
    session = MagicMock()
    session.get.side_effect = requests.exceptions.ConnectionError()
    mock_build.return_value = session
    with pytest.raises(BreachCheckError):
        check_breaches("someone@example.com")


@patch("whereami.breach.build_session")
def test_api_key_never_sent_as_query_param(mock_build, monkeypatch):
    monkeypatch.setenv("HIBP_API_KEY", "super-secret-key")
    session = _mock_session(404)
    mock_build.return_value = session
    check_breaches("someone@example.com")
    called_url = session.get.call_args[0][0]
    assert "super-secret-key" not in called_url
    assert session.get.call_args[1]["headers"]["hibp-api-key"] == "super-secret-key"
