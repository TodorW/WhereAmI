import pytest

from whereami.sites import SITES, Category, Site, sites_by_category


def test_no_duplicate_site_names():
    names = [site.name for site in SITES]
    assert len(names) == len(set(names))


def test_every_site_uses_https():
    for site in SITES:
        assert site.url_template.startswith("https://"), site.name


def test_every_site_template_has_value_placeholder():
    for site in SITES:
        assert "{value}" in site.url_template, site.name


def test_every_site_is_reachable_through_its_category_grouping():
    grouped = sites_by_category()
    all_grouped_names = {site.name for entries in grouped.values() for site in entries}
    assert all_grouped_names == {site.name for site in SITES}


def test_no_homepage_only_urls():
    # A URL that resolves to a fixed page regardless of {value} always
    # returns the same status code, which is a guaranteed false signal.
    for site in SITES:
        rendered_a = site.url_template.format(value="account-that-should-not-exist-zzz")
        rendered_b = site.url_template.format(value="a-totally-different-value-yyy")
        assert rendered_a != rendered_b, site.name


def test_rejects_non_https_template():
    with pytest.raises(ValueError):
        Site("Bad", Category.SOCIAL, "http://example.com/{value}", "high")


def test_rejects_missing_placeholder():
    with pytest.raises(ValueError):
        Site("Bad", Category.SOCIAL, "https://example.com/profile", "high")
