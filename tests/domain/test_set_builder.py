import pytest

from vinyl_set_builder.domain.exceptions import IncompatibleCrateError
from vinyl_set_builder.domain.models import Track
from vinyl_set_builder.domain.set_builder import build_set_order


def test_build_set_order_raises_with_fewer_than_two_tracks():
    tracks = [Track(id=1, artist="A", title="T1", bpm=120.0, key="8A", genre="house")]
    with pytest.raises(IncompatibleCrateError):
        build_set_order(tracks)


def test_build_set_order_raises_when_no_pair_is_compatible():
    tracks = [
        Track(id=1, artist="A", title="T1", bpm=90.0, key="1A", genre="house"),
        Track(id=2, artist="B", title="T2", bpm=175.0, key="7B", genre="dnb"),
    ]
    with pytest.raises(IncompatibleCrateError):
        build_set_order(tracks)


def test_build_set_order_chains_compatible_tracks_without_hard_cuts():
    tracks = [
        Track(id=1, artist="A", title="T1", bpm=120.0, key="8A", genre="house"),
        Track(id=2, artist="B", title="T2", bpm=121.0, key="8A", genre="house"),
        Track(id=3, artist="C", title="T3", bpm=122.0, key="9A", genre="house"),
    ]
    order, transitions = build_set_order(tracks)
    assert [t.id for t in order] == [1, 2, 3]
    assert all(not t.is_hard_cut for t in transitions)
    assert len(transitions) == 2


def test_build_set_order_marks_hard_cut_when_no_compatible_neighbor_left():
    tracks = [
        Track(id=1, artist="A", title="T1", bpm=120.0, key="8A", genre="house"),
        Track(id=2, artist="B", title="T2", bpm=121.0, key="8A", genre="house"),
        Track(id=3, artist="C", title="T3", bpm=175.0, key="3B", genre="dnb"),
    ]
    order, transitions = build_set_order(tracks)
    assert len(order) == 3
    assert any(t.is_hard_cut for t in transitions)
