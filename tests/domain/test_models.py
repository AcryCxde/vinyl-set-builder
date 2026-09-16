import pytest

from vinyl_set_builder.domain.exceptions import InvalidCamelotKeyError
from vinyl_set_builder.domain.models import Track, are_keys_compatible, parse_camelot_key


def make_track(**overrides):
    defaults = dict(id=1, artist="DJ Shadow", title="Building Steam", bpm=91.0, key="8A", genre="trip-hop")
    defaults.update(overrides)
    return Track(**defaults)


def test_track_coordinate_is_a_bpm_key_tuple():
    track = make_track(bpm=120.0, key="5B")
    assert track.coordinate == (120.0, "5B")


def test_track_tags_default_to_an_empty_set():
    track = make_track()
    assert track.tags == set()
    assert isinstance(track.tags, set)


def test_track_accepts_explicit_tags_as_a_set():
    track = make_track(tags={"dark", "energy:high"})
    assert track.tags == {"dark", "energy:high"}


def test_track_rejects_invalid_camelot_key():
    with pytest.raises(InvalidCamelotKeyError):
        make_track(key="not-a-key")


@pytest.mark.parametrize(
    "key,expected",
    [("8A", (8, "A")), ("12B", (12, "B")), ("1A", (1, "A"))],
)
def test_parse_camelot_key_valid(key, expected):
    assert parse_camelot_key(key) == expected


@pytest.mark.parametrize("key", ["H1", "13A", "0B", "8", "A8", ""])
def test_parse_camelot_key_invalid_raises(key):
    with pytest.raises(InvalidCamelotKeyError):
        parse_camelot_key(key)


@pytest.mark.parametrize(
    "key_a,key_b",
    [
        ("8A", "8A"),   # идентичные
        ("8A", "8B"),   # параллельный мажор/минор
        ("8A", "9A"),   # соседний номер, та же буква
        ("8A", "7A"),   # соседний номер, та же буква (в другую сторону)
        ("12A", "1A"),  # переход по кругу
    ],
)
def test_compatible_key_pairs(key_a, key_b):
    assert are_keys_compatible(key_a, key_b) is True


@pytest.mark.parametrize(
    "key_a,key_b",
    [
        ("8A", "10A"),  # слишком далеко друг от друга по кругу
        ("8A", "9B"),   # соседний номер, но другая буква
        ("8A", "3A"),   # противоположная сторона круга
    ],
)
def test_incompatible_key_pairs(key_a, key_b):
    assert are_keys_compatible(key_a, key_b) is False
