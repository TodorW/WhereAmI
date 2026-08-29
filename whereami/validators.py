"""Input validation for user-supplied identifiers.

Keeping this strict matters: whatever passes here gets URL-encoded and
dropped straight into request paths against ~50 live hosts.
"""

import re

_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
_USERNAME_RE = re.compile(r"^[A-Za-z0-9._\-]{1,39}$")

MAX_EMAIL_LENGTH = 254
MAX_USERNAME_LENGTH = 39


class ValidationError(ValueError):
    """Raised when a user-supplied identifier fails validation."""


def validate_email(value: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValidationError("email address cannot be empty")
    if len(value) > MAX_EMAIL_LENGTH:
        raise ValidationError(f"email address exceeds {MAX_EMAIL_LENGTH} characters")
    if not _EMAIL_RE.match(value):
        raise ValidationError(f"'{value}' is not a valid email address")
    return value


def validate_username(value: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValidationError("username cannot be empty")
    if len(value) > MAX_USERNAME_LENGTH:
        raise ValidationError(f"username exceeds {MAX_USERNAME_LENGTH} characters")
    if not _USERNAME_RE.match(value):
        raise ValidationError(
            f"'{value}' is not a valid username "
            "(letters, numbers, '.', '_', '-' only)"
        )
    return value


def email_local_part(email: str) -> str:
    """Best-effort username guess derived from the part before the '@'."""
    return email.split("@", 1)[0]
