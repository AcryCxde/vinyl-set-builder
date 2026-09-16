import pytest

from vinyl_set_builder.domain.exceptions import InvalidCamelotKeyError
from vinyl_set_builder.domain.models import are_keys_compatible, parse_camelot_key


def test_track_coordinate_is_a_bpm_key_tuple(make_track):
    track = make_track(bpm=120.0, key="5B")
    assert track.coordinate == (120.0, "5B")


@pytest.mark.parametrize(
    ("tags_kwarg", "expected"),
    [
        pytest.param(None, set(), id="defaults_to_empty_set"),
        pytest.param({"dark", "energy:high"}, {"dark", "energy:high"}, id="accepts_explicit_tags"),
    ],
)
def test_track_tags(make_track, tags_kwarg, expected):
    track = make_track(tags=tags_kwarg)
    assert track.tags == expected
    assert isinstance(track.tags, set)


def test_track_rejects_invalid_camelot_key(make_track):
    with pytest.raises(InvalidCamelotKeyError):
        make_track(key="not-a-key")


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        pytest.param("8A", (8, "A"), id="number_and_letter"),
        pytest.param("12B", (12, "B"), id="two_digit_number"),
        pytest.param("1A", (1, "A"), id="single_digit_number"),
    ],
)
def test_parse_camelot_key_valid(key, expected):
    assert parse_camelot_key(key) == expected


@pytest.mark.parametrize(
    "key",
    [
        pytest.param("H1", id="letter_first"),
        pytest.param("13A", id="number_out_of_range_high"),
        pytest.param("0B", id="number_out_of_range_low"),
        pytest.param("8", id="missing_letter"),
        pytest.param("A8", id="reversed_order"),
        pytest.param("", id="empty_string"),
    ],
)
def test_parse_camelot_key_invalid_raises(key):
    with pytest.raises(InvalidCamelotKeyError):
        parse_camelot_key(key)


@pytest.mark.parametrize(
    ("key_a", "key_b", "expected"),
    [
        pytest.param("8A", "8A", True, id="identical"),
        pytest.param("8A", "8B", True, id="relative_major_minor"),
        pytest.param("8A", "9A", True, id="adjacent_number_same_letter"),
        pytest.param("8A", "7A", True, id="adjacent_number_same_letter_other_direction"),
        pytest.param("12A", "1A", True, id="wheel_wraps_around"),
        pytest.param("8A", "10A", False, id="too_far_apart_on_the_wheel"),
        pytest.param("8A", "9B", False, id="adjacent_number_different_letter"),
        pytest.param("8A", "3A", False, id="opposite_side_of_the_wheel"),
    ],
)
def test_are_keys_compatible(key_a, key_b, expected):
    assert are_keys_compatible(key_a, key_b) is expected
