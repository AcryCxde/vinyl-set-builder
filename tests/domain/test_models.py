import pytest

from vinyl_set_builder.domain.exceptions import InvalidCamelotKeyError
from vinyl_set_builder.domain.models import are_keys_compatible, parse_camelot_key


def test_parse_camelot_key_splits_number_and_letter():
    assert parse_camelot_key("12B") == (12, "B")


@pytest.mark.parametrize("key", ["13A", "0B", "8", "A8", ""])
def test_parse_camelot_key_rejects_invalid_format(key):
    with pytest.raises(InvalidCamelotKeyError):
        parse_camelot_key(key)


def test_track_rejects_invalid_camelot_key(make_track):
    with pytest.raises(InvalidCamelotKeyError):
        make_track(key="not-a-key")


@pytest.mark.parametrize(
    ("key_a", "key_b", "expected"),
    [
        pytest.param("8A", "8B", True, id="relative_major_minor"),
        pytest.param("8A", "9A", True, id="adjacent_number_same_letter"),
        pytest.param("12A", "1A", True, id="wheel_wraps_around"),
        pytest.param("8A", "9B", False, id="adjacent_number_different_letter"),
        pytest.param("8A", "10A", False, id="too_far_apart"),
    ],
)
def test_are_keys_compatible(key_a, key_b, expected):
    assert are_keys_compatible(key_a, key_b) is expected
