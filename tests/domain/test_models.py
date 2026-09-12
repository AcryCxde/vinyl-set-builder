import pytest

from vinyl_set_builder.domain.exceptions import InvalidCamelotKeyError
from vinyl_set_builder.domain.models import Track


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
