"""Exporting scan results to disk (or stdout via path "-").

Nothing is written unless the caller explicitly asks for a path — the tool
never persists scanned identifiers on its own.
"""

import csv
import json
import sys
from pathlib import Path

from .checker import CheckResult

STDOUT_PATH = "-"


def _result_to_dict(result: CheckResult) -> dict:
    return {
        "site": result.site.name,
        "category": result.site.category.value,
        "confidence": result.site.confidence.value,
        "verdict": result.verdict.value,
        "detail": result.detail,
        "url": result.url,
    }


def export_json(results: list[CheckResult], path: str) -> None:
    payload = json.dumps([_result_to_dict(result) for result in results], indent=2)
    if path == STDOUT_PATH:
        print(payload)
        return
    Path(path).write_text(payload, encoding="utf-8")


def export_csv(results: list[CheckResult], path: str) -> None:
    fieldnames = ["site", "category", "confidence", "verdict", "detail", "url"]

    def _write(handle):
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(_result_to_dict(result))

    if path == STDOUT_PATH:
        _write(sys.stdout)
        return
    with open(path, "w", newline="", encoding="utf-8") as handle:
        _write(handle)
