"""Concurrent execution of site checks."""

from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Semaphore
from urllib.parse import quote, urlparse

from .checker import CheckResult, check_site
from .http_client import DEFAULT_TIMEOUT_SECONDS, build_session
from .sites import Site

DEFAULT_MAX_WORKERS = 8
MAX_ALLOWED_WORKERS = 20
DEFAULT_PER_HOST_CONCURRENCY = 2


def _host_for(site: Site, value: str) -> str:
    rendered = site.url_template.format(value=quote(value, safe=""))
    return urlparse(rendered).netloc


def run_checks(
    sites: Iterable[Site],
    value: str,
    max_workers: int = DEFAULT_MAX_WORKERS,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    on_result: Callable[[CheckResult], None] | None = None,
    per_host_concurrency: int = DEFAULT_PER_HOST_CONCURRENCY,
) -> list[CheckResult]:
    sites = list(sites)
    max_workers = max(1, min(max_workers, MAX_ALLOWED_WORKERS))
    per_host_concurrency = max(1, per_host_concurrency)
    session = build_session()
    results: list[CheckResult] = []

    # Built up-front in the main thread so no two workers can race to create
    # a semaphore for the same host.
    host_by_site = {site.name: _host_for(site, value) for site in sites}
    semaphore_by_host = {host: Semaphore(per_host_concurrency) for host in set(host_by_site.values())}

    def _bounded_check(site: Site) -> CheckResult:
        with semaphore_by_host[host_by_site[site.name]]:
            return check_site(session, site, value, timeout)

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_bounded_check, site): site for site in sites}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if on_result:
                on_result(result)

    return results
