"""Console rendering of scan results."""

import sys
from collections import Counter

from .checker import CheckResult, Verdict

_ICONS = {
    Verdict.FOUND: "✓",
    Verdict.NOT_FOUND: "✗",
    Verdict.UNCERTAIN: "?",
    Verdict.ERROR: "!",
}


class Colors:
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    DIM = "\033[2m"
    RESET = "\033[0m"


_COLOR_BY_VERDICT = {
    Verdict.FOUND: Colors.GREEN,
    Verdict.NOT_FOUND: Colors.RED,
    Verdict.UNCERTAIN: Colors.YELLOW,
    Verdict.ERROR: Colors.DIM,
}


def supports_color(stream=sys.stdout) -> bool:
    return hasattr(stream, "isatty") and stream.isatty()


def format_result_line(result: CheckResult, use_color: bool = True) -> str:
    icon = _ICONS[result.verdict]
    confidence_tag = f" ({result.site.confidence.value} confidence)" if result.verdict == Verdict.FOUND else ""
    line = f"{icon} {result.site.name}{confidence_tag} - {result.detail}"
    if not use_color:
        return line
    color = _COLOR_BY_VERDICT[result.verdict]
    return f"{color}{line}{Colors.RESET}"


def summarize(results: list[CheckResult]) -> Counter:
    return Counter(result.verdict for result in results)
