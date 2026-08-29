"""Command-line entry point."""

import argparse
import sys

from . import __version__
from .checker import Verdict
from .concurrency import DEFAULT_MAX_WORKERS, MAX_ALLOWED_WORKERS, run_checks
from .export import export_csv, export_json
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
        help="limit the scan to one category (repeatable)",
    )
    parser.add_argument(
        "--only-found", action="store_true", help="only print sites where an account was found"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_MAX_WORKERS,
        help=f"concurrent requests (default {DEFAULT_MAX_WORKERS}, max {MAX_ALLOWED_WORKERS})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"per-request timeout in seconds (default {DEFAULT_TIMEOUT_SECONDS})",
    )
    parser.add_argument("--output", help="write results to this file")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="format for --output")
    parser.add_argument("--no-color", action="store_true", help="disable colored output")
    parser.add_argument("--list-categories", action="store_true", help="list available categories and exit")
    return parser


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


def select_sites(args: argparse.Namespace) -> list:
    sites = SITES
    if args.category:
        wanted = set(args.category)
        sites = [site for site in sites if site.category.value in wanted]
    return sites


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_categories:
        for category in Category:
            print(category.value)
        return 0

    try:
        value = resolve_identity(args)
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    sites = select_sites(args)
    if not sites:
        print("error: no sites match the requested category filter", file=sys.stderr)
        return 1

    use_color = supports_color() and not args.no_color
    print(f"Checking '{value}' against {len(sites)} sites...\n")

    def on_result(result):
        if args.only_found and result.verdict != Verdict.FOUND:
            return
        print(format_result_line(result, use_color=use_color))

    results = run_checks(sites, value, max_workers=args.workers, timeout=args.timeout, on_result=on_result)

    counts = summarize(results)
    print("\n--- Summary ---")
    print(f"Found:     {counts.get(Verdict.FOUND, 0)}")
    print(f"Not found: {counts.get(Verdict.NOT_FOUND, 0)}")
    print(f"Uncertain: {counts.get(Verdict.UNCERTAIN, 0)}")
    print(f"Errors:    {counts.get(Verdict.ERROR, 0)}")

    if args.output:
        exporter = export_json if args.format == "json" else export_csv
        exporter(results, args.output)
        print(f"\nResults written to {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
