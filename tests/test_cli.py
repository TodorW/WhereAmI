import json
from unittest.mock import patch

import pytest

from whereami import cli
from whereami.checker import CheckResult, Verdict
from whereami.sites import SITES, Category, Confidence, Site

SITE = Site("GitHub", Category.DEVELOPMENT, "https://api.github.com/users/{value}", Confidence.HIGH)


def _fake_run_checks(sites, value, max_workers, timeout, on_result=None, per_host_concurrency=2):
    result = CheckResult(SITE, Verdict.FOUND, "status 200", "https://api.github.com/users/x")
    if on_result:
        on_result(result)
    return [result]


def test_list_categories_exits_zero(capsys):
    exit_code = cli.main(["--list-categories"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Development" in out


def test_invalid_username_returns_error(capsys):
    exit_code = cli.main(["--username", "bad username with spaces"])
    assert exit_code == 1
    assert "error" in capsys.readouterr().err


def test_invalid_email_returns_error(capsys):
    exit_code = cli.main(["--email", "not-an-email"])
    assert exit_code == 1


@patch("whereami.cli.run_checks", side_effect=_fake_run_checks)
def test_username_scan_prints_summary(mock_run, capsys):
    exit_code = cli.main(["--username", "torvalds", "--no-color"])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "GitHub" in out
    assert "Found:     1" in out


@patch("whereami.cli.run_checks", side_effect=_fake_run_checks)
def test_email_uses_local_part_as_username(mock_run, capsys):
    cli.main(["--email", "torvalds@example.com", "--no-color"])
    called_value = mock_run.call_args[0][1]
    assert called_value == "torvalds"


def test_unknown_category_filter_rejected_by_argparse():
    with pytest.raises(SystemExit):
        cli.main(["--username", "x", "--category", "Not A Real Category"])


def test_select_sites_filters_by_category():
    selected = cli.select_sites(["Development"])
    assert selected
    assert all(site.category.value == "Development" for site in selected)


def test_select_sites_with_no_filter_returns_all():
    assert cli.select_sites(None) == SITES


@patch("whereami.cli.run_checks", side_effect=_fake_run_checks)
def test_diff_reports_new_hit(mock_run, capsys, tmp_path):
    previous = tmp_path / "previous.json"
    previous.write_text(json.dumps([]), encoding="utf-8")

    exit_code = cli.main(["--username", "torvalds", "--no-color", "--diff", str(previous)])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "New: GitHub" in out


@patch("whereami.cli.run_checks", side_effect=_fake_run_checks)
def test_diff_with_missing_file_errors(mock_run, capsys):
    exit_code = cli.main(["--username", "torvalds", "--no-color", "--diff", "/nope.json"])
    assert exit_code == 1
    assert "error" in capsys.readouterr().err
