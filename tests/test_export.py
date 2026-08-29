import csv
import json

from whereami.checker import CheckResult, Verdict
from whereami.export import export_csv, export_json
from whereami.sites import Category, Confidence, Site

SITE = Site("GitHub", Category.DEVELOPMENT, "https://api.github.com/users/{value}", Confidence.HIGH)
RESULTS = [CheckResult(SITE, Verdict.FOUND, "status 200", "https://api.github.com/users/x")]


def test_export_json_writes_expected_fields(tmp_path):
    out = tmp_path / "out.json"
    export_json(RESULTS, str(out))
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data == [
        {
            "site": "GitHub",
            "category": "Development",
            "confidence": "high",
            "verdict": "found",
            "detail": "status 200",
            "url": "https://api.github.com/users/x",
        }
    ]


def test_export_csv_writes_expected_rows(tmp_path):
    out = tmp_path / "out.csv"
    export_csv(RESULTS, str(out))
    with open(out, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["site"] == "GitHub"
    assert rows[0]["verdict"] == "found"


def test_export_json_to_stdout(capsys):
    export_json(RESULTS, "-")
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data[0]["site"] == "GitHub"


def test_export_csv_to_stdout(capsys):
    export_csv(RESULTS, "-")
    out = capsys.readouterr().out
    rows = list(csv.DictReader(out.splitlines()))
    assert rows[0]["site"] == "GitHub"
