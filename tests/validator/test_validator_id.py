import pytest

from rick.validator import Validator

FIELD_NAME = "field1"

# str.isnumeric() is true for the whole Unicode numeric family. int() accepts
# only the decimal-digit part of it, so guarding an int() call with isnumeric()
# raised ValueError from inside validation instead of returning a validation
# failure.
raising_before = ["½", "⅓", "²", "Ⅷ"]

# non-ASCII decimal digits. int() accepts these, so they never raised — they
# were silently admitted as ids. An id is a database key; the accepted set is
# [0-9], so these are invalid too.
non_ascii_decimals = ["٣", "๓"]


@pytest.mark.parametrize("value", raising_before)
def test_id_rejects_non_decimal_numerics(value):
    assert Validator({FIELD_NAME: "id"}).is_valid({FIELD_NAME: value}) is False


@pytest.mark.parametrize("value", raising_before)
def test_idlist_rejects_non_decimal_numerics(value):
    assert Validator({FIELD_NAME: "idlist"}).is_valid({FIELD_NAME: [value]}) is False


@pytest.mark.parametrize("value", non_ascii_decimals)
def test_id_rejects_non_ascii_decimal_digits(value):
    assert Validator({FIELD_NAME: "id"}).is_valid({FIELD_NAME: value}) is False


@pytest.mark.parametrize("value", non_ascii_decimals)
def test_idlist_rejects_non_ascii_decimal_digits(value):
    assert Validator({FIELD_NAME: "idlist"}).is_valid({FIELD_NAME: [value]}) is False


@pytest.mark.parametrize(
    "value,expected",
    [("5", True), ("1", True), ("0", False), ("-1", False), ("abc", False), ("", False)],
)
def test_id_ascii_behaviour_unchanged(value, expected):
    assert Validator({FIELD_NAME: "id"}).is_valid({FIELD_NAME: value}) is expected
