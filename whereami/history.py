"""Comparing a scan against a previous JSON export.

Only JSON exports are supported as diff input: the format is stable and
trivially parseable, unlike CSV's quoting edge cases.
"""

import json
from pathlib import Path

from .checker import CheckResult, Verdict


class HistoryError(RuntimeError):
    pass


def load_previous_founds(path: str) -> set[str]:
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise HistoryError(f"could not read '{path}': {exc.strerror}") from exc

    try:
        entries = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HistoryError(f"'{path}' is not valid JSON: {exc}") from exc

    if not isinstance(entries, list):
        raise HistoryError(f"'{path}' does not look like a whereami JSON export")

    return {entry["site"] for entry in entries if entry.get("verdict") == Verdict.FOUND.value}


def diff_founds(previous_founds: set[str], results: list[CheckResult]) -> tuple[set[str], set[str]]:
    current_founds = {result.site.name for result in results if result.verdict == Verdict.FOUND}
    new = current_founds - previous_founds
    lost = previous_founds - current_founds
    return new, lost
