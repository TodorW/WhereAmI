from whereami.checker import CheckResult, Verdict
from whereami.report import format_result_line, group_by_category, summarize
from whereami.sites import Category, Confidence, Site

GITHUB = Site("GitHub", Category.DEVELOPMENT, "https://api.github.com/users/{value}", Confidence.HIGH)
REDDIT = Site("Reddit", Category.SOCIAL, "https://www.reddit.com/user/{value}/about.json", Confidence.HIGH)


def test_format_result_line_without_color_has_no_escape_codes():
    result = CheckResult(GITHUB, Verdict.FOUND, "status 200", "https://x")
    line = format_result_line(result, use_color=False)
    assert "\033" not in line
    assert "GitHub" in line
    assert "high confidence" in line


def test_format_result_line_with_color_wraps_in_escape_codes():
    result = CheckResult(GITHUB, Verdict.FOUND, "status 200", "https://x")
    line = format_result_line(result, use_color=True)
    assert "\033" in line


def test_not_found_has_no_confidence_tag():
    result = CheckResult(GITHUB, Verdict.NOT_FOUND, "status 404", "https://x")
    line = format_result_line(result, use_color=False)
    assert "confidence" not in line


def test_summarize_counts_verdicts():
    results = [
        CheckResult(GITHUB, Verdict.FOUND, "", ""),
        CheckResult(REDDIT, Verdict.NOT_FOUND, "", ""),
    ]
    counts = summarize(results)
    assert counts[Verdict.FOUND] == 1
    assert counts[Verdict.NOT_FOUND] == 1


def test_group_by_category():
    results = [
        CheckResult(GITHUB, Verdict.FOUND, "", ""),
        CheckResult(REDDIT, Verdict.NOT_FOUND, "", ""),
    ]
    grouped = group_by_category(results)
    assert grouped[Category.DEVELOPMENT.value][0].site.name == "GitHub"
    assert grouped[Category.SOCIAL.value][0].site.name == "Reddit"
