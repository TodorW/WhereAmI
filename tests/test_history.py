import json

import pytest

from whereami.checker import CheckResult, Verdict
from whereami.history import HistoryError, diff_founds, load_previous_founds
from whereami.sites import Category, Confidence, Site

GITHUB = Site("GitHub", Category.DEVELOPMENT, "https://x/{value}", Confidence.HIGH)
NPM = Site("npm", Category.DEVELOPMENT, "https://y/{value}", Confidence.HIGH)


def _write(tmp_path, data):
    path = tmp_path / "prev.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


def test_load_previous_founds_only_keeps_found_entries(tmp_path):
    data = [
        {"site": "GitHub", "verdict": "found"},
        {"site": "Reddit", "verdict": "not_found"},
    ]
    path = _write(tmp_path, data)
    assert load_previous_founds(path) == {"GitHub"}


def test_load_previous_founds_missing_file_raises():
    with pytest.raises(HistoryError):
        load_previous_founds("/definitely/does/not/exist.json")


def test_load_previous_founds_bad_json_raises(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(HistoryError):
        load_previous_founds(str(path))


def test_load_previous_founds_wrong_shape_raises(tmp_path):
    path = tmp_path / "wrong.json"
    path.write_text(json.dumps({"not": "a list"}), encoding="utf-8")
    with pytest.raises(HistoryError):
        load_previous_founds(str(path))


def test_diff_founds_reports_new_and_lost():
    previous = {"GitHub", "Reddit"}
    results = [CheckResult(GITHUB, Verdict.FOUND, "", ""), CheckResult(NPM, Verdict.FOUND, "", "")]
    new, lost = diff_founds(previous, results)
    assert new == {"npm"}
    assert lost == {"Reddit"}


def test_diff_founds_no_changes():
    previous = {"GitHub"}
    results = [CheckResult(GITHUB, Verdict.FOUND, "", "")]
    new, lost = diff_founds(previous, results)
    assert new == set()
    assert lost == set()
