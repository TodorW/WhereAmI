from unittest.mock import patch

from whereami.checker import CheckResult, Verdict
from whereami.concurrency import MAX_ALLOWED_WORKERS, run_checks
from whereami.sites import Category, Confidence, Site

SITES = [
    Site(f"Site{i}", Category.SOCIAL, "https://example.com/{value}", Confidence.MEDIUM)
    for i in range(5)
]


def _fake_check_site(session, site, value, timeout):
    return CheckResult(site, Verdict.FOUND, "status 200", "https://example.com/x")


@patch("whereami.concurrency.build_session")
@patch("whereami.concurrency.check_site", side_effect=_fake_check_site)
def test_run_checks_returns_one_result_per_site(mock_check, mock_session):
    results = run_checks(SITES, "someone", max_workers=3)
    assert len(results) == len(SITES)
    assert all(r.verdict == Verdict.FOUND for r in results)


@patch("whereami.concurrency.build_session")
@patch("whereami.concurrency.check_site", side_effect=_fake_check_site)
def test_on_result_callback_is_invoked_per_site(mock_check, mock_session):
    seen = []
    run_checks(SITES, "someone", max_workers=3, on_result=seen.append)
    assert len(seen) == len(SITES)


@patch("whereami.concurrency.build_session")
@patch("whereami.concurrency.check_site", side_effect=_fake_check_site)
def test_worker_count_is_capped(mock_check, mock_session):
    # Should not raise or hang even when asked for an absurd worker count.
    results = run_checks(SITES, "someone", max_workers=MAX_ALLOWED_WORKERS * 100)
    assert len(results) == len(SITES)
