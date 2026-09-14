import pytest
from pydantic import ValidationError

from vinyl_set_builder.api.schemas import TrackCreate


def test_track_create_accepts_valid_payload():
    payload = TrackCreate(artist="A", title="T1", bpm=120.0, key="8A", genre="house", tags={"dark"})
    assert payload.tags == {"dark"}


def test_track_create_defaults_tags_to_empty_set():
    payload = TrackCreate(artist="A", title="T1", bpm=120.0, key="8A", genre="house")
    assert payload.tags == set()


def test_track_create_rejects_non_positive_bpm():
    with pytest.raises(ValidationError):
        TrackCreate(artist="A", title="T1", bpm=0, key="8A", genre="house")
