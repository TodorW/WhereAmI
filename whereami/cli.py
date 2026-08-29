"""Command-line entry point."""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from . import __version__
from .checker import Verdict
from .concurrency import DEFAULT_MAX_WORKERS, DEFAULT_PER_HOST_CONCURRENCY, MAX_ALLOWED_WORKERS, run_checks
from .config import ConfigError, load_config
from .export import export_csv, export_json
from .history import HistoryError, diff_founds, load_previous_founds
from .http_client import DEFAULT_TIMEOUT_SECONDS
from .report import format_result_line, summarize, supports_color
from .sites import SITES, Category
from .validators import ValidationError, email_local_part, validate_email, validate_username


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="whereami",
        description="Check which sites have a public profile for a username or email's local part.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    identity = parser.add_mutually_exclusive_group()
    identity.add_argument("--username", help="username to check across sites")
    identity.add_argument("--email", help="email address; the part before '@' is used as the username")
    parser.add_argument(
        "--category",
        action="append",
        choices=[c.value for c in Category],
        help="limit the scan to one category (repeatable); overrides config file categories",
    )
    parser.add_argument(
        "--only-found",
        action="store_true",
        default=None,
        help="only print sites where an account was found",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help=f"concurrent requests (default {DEFAULT_MAX_WORKERS}, max {MAX_ALLOWED_WORKERS})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help=f"per-request timeout in seconds (default {DEFAULT_TIMEOUT_SECONDS})",
    )
    parser.add_argument(
        "--host-concurrency",
        type=int,
        default=None,
        help=f"max simultaneous requests to the same host (default {DEFAULT_PER_HOST_CONCURRENCY})",
    )
    parser.add_argument(
        "--diff",
        metavar="PREVIOUS_JSON",
        help="compare against a previous --output json export and show what changed",
    )
    parser.add_argument("--output", help="write results to this file, or '-' for stdout")
    parser.add_argument("--format", choices=["json", "csv"], default=None, help="format for --output")
    parser.add_argument("--no-color", action="store_true", default=None, help="disable colored output")
    parser.add_argument(
        "--quiet", action="store_true", help="suppress progress and summary output (only --output prints)"
    )
    parser.add_argument(
        "--config", metavar="PATH", help="path to a config file (default: ~/.whereami.toml if present)"
    )
    parser.add_argument("--list-categories", action="store_true", help="list available categories and exit")
    return parser


@dataclass
class Settings:
    workers: int
    timeout: int
    host_concurrency: int
    only_found: bool
    no_color: bool
    output_format: str
    categories: list[str] | None


def _pick(cli_value, config: dict, key: str, default):
    return cli_value if cli_value is not None else config.get(key, default)


def resolve_settings(args: argparse.Namespace, config: dict) -> Settings:
    categories = _pick(args.category, config, "categories", None)
    if categories is not None:
        unknown = set(categories) - {c.value for c in Category}
        if unknown:
            noun = "category" if len(unknown) == 1 else "categories"
            raise ConfigError(f"unknown {noun}: {', '.join(sorted(unknown))}")

    output_format = _pick(args.format, config, "format", "json")
    if output_format not in ("json", "csv"):
        raise ConfigError(f"format must be 'json' or 'csv', got '{output_format}'")

    try:
        return Settings(
            workers=int(_pick(args.workers, config, "workers", DEFAULT_MAX_WORKERS)),
            timeout=int(_pick(args.timeout, config, "timeout", DEFAULT_TIMEOUT_SECONDS)),
            host_concurrency=int(
                _pick(args.host_concurrency, config, "host_concurrency", DEFAULT_PER_HOST_CONCURRENCY)
            ),
            only_found=bool(_pick(args.only_found, config, "only_found", False)),
            no_color=bool(_pick(args.no_color, config, "no_color", False)),
            output_format=output_format,
            categories=categories,
        )
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"invalid setting: {exc}") from exc


def resolve_identity(args: argparse.Namespace) -> str:
    if args.username:
        return validate_username(args.username)
    if args.email:
        email = validate_email(args.email)
        return validate_username(email_local_part(email))

    raw = input("Enter a username (or email) to check: ").strip()
    if "@" in raw:
        return validate_username(email_local_part(validate_email(raw)))
    return validate_username(raw)


def select_sites(categories: list[str] | None) -> list:
    if not categories:
        return SITES
    wanted = set(categories)
    return [site for site in SITES if site.category.value in wanted]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_categories:
        for category in Category:
            print(category.value)
        return 0

    try:
        config = load_config(Path(args.config) if args.config else None)
        settings = resolve_settings(args, config)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        value = resolve_identity(args)
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    sites = select_sites(settings.categories)
    if not sites:
        print("error: no sites match the requested category filter", file=sys.stderr)
        return 1

    use_color = supports_color() and not settings.no_color
    quiet = args.quiet

    if not quiet:
        print(f"Checking '{value}' against {len(sites)} sites...\n")

    def on_result(result):
        if quiet:
            return
        if settings.only_found and result.verdict != Verdict.FOUND:
            return
        print(format_result_line(result, use_color=use_color))

    results = run_checks(
        sites,
        value,
        max_workers=settings.workers,
        timeout=settings.timeout,
        on_result=on_result,
        per_host_concurrency=settings.host_concurrency,
    )

    if not quiet:
        counts = summarize(results)
        print("\n--- Summary ---")
        print(f"Found:     {counts.get(Verdict.FOUND, 0)}")
        print(f"Not found: {counts.get(Verdict.NOT_FOUND, 0)}")
        print(f"Uncertain: {counts.get(Verdict.UNCERTAIN, 0)}")
        print(f"Errors:    {counts.get(Verdict.ERROR, 0)}")

    if args.diff:
        try:
            previous_founds = load_previous_founds(args.diff)
        except HistoryError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        new, lost = diff_founds(previous_founds, results)
        if not quiet:
            print("\n--- Changes since last scan ---")
            if new:
                print(f"New: {', '.join(sorted(new))}")
            if lost:
                print(f"Lost: {', '.join(sorted(lost))}")
            if not new and not lost:
                print("No change")

    if args.output:
        exporter = export_json if settings.output_format == "json" else export_csv
        exporter(results, args.output)
        if not quiet and args.output != "-":
            print(f"\nResults written to {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
