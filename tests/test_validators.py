import pytest

from whereami.validators import (
    ValidationError,
    email_local_part,
    validate_email,
    validate_username,
)


def test_validate_email_accepts_normal_address():
    assert validate_email(" person@example.com ") == "person@example.com"


@pytest.mark.parametrize(
    "bad",
    ["", "   ", "not-an-email", "person@", "@example.com", "a" * 260 + "@example.com"],
)
def test_validate_email_rejects_bad_input(bad):
    with pytest.raises(ValidationError):
        validate_email(bad)


def test_validate_username_accepts_normal_username():
    assert validate_username(" cool.user-1 ") == "cool.user-1"


@pytest.mark.parametrize("bad", ["", "   ", "has spaces", "semi;colon", "a" * 40])
def test_validate_username_rejects_bad_input(bad):
    with pytest.raises(ValidationError):
        validate_username(bad)


def test_email_local_part():
    assert email_local_part("person@example.com") == "person"
