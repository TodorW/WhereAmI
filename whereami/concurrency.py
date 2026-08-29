"""Concurrent execution of site checks."""

from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed

from .checker import CheckResult, check_site
from .http_client import DEFAULT_TIMEOUT_SECONDS, build_session
from .sites import Site

DEFAULT_MAX_WORKERS = 8


def run_checks(
    sites: Iterable[Site],
    value: str,
    max_workers: int = DEFAULT_MAX_WORKERS,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    on_result: Callable[[CheckResult], None] | None = None,
) -> list[CheckResult]:
    sites = list(sites)
    session = build_session()
    results: list[CheckResult] = []

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(check_site, session, site, value, timeout): site for site in sites}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if on_result:
                on_result(result)

    return results
