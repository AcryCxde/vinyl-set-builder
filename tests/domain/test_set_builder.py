import inspect

import pytest

from vinyl_set_builder.domain.exceptions import IncompatibleCrateError
from vinyl_set_builder.domain.models import Track
from vinyl_set_builder.domain.set_builder import (
    SetOrder,
    SetStep,
    build_compatibility_graph,
    build_set_order,
    iter_compatible_pairs,
)


def make_tracks():
    return [
        Track(id=1, artist="A", title="T1", bpm=120.0, key="8A", genre="house"),
        Track(id=2, artist="B", title="T2", bpm=121.0, key="8A", genre="house"),   # совместим с 1
        Track(id=3, artist="C", title="T3", bpm=150.0, key="3B", genre="techno"),  # ни с кем не совместим
    ]


def test_iter_compatible_pairs_is_a_generator():
    result = iter_compatible_pairs(make_tracks())
    assert inspect.isgenerator(result)


def test_iter_compatible_pairs_yields_only_compatible_pairs():
    pairs = list(iter_compatible_pairs(make_tracks()))
    ids = [(a.id, b.id) for a, b in pairs]
    assert ids == [(1, 2)]


def test_build_compatibility_graph_is_symmetric():
    graph = build_compatibility_graph(make_tracks())
    assert graph[1] == {2}
    assert graph[2] == {1}
    assert graph[3] == set()


def test_build_compatibility_graph_respects_bpm_tolerance():
    tracks = make_tracks()
    graph = build_compatibility_graph(tracks, bpm_tolerance=0.5)
    assert graph[1] == set()  # 120.0 против 121.0 теперь вне допуска


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


def make_chain_tracks():
    return [
        Track(id=1, artist="A", title="T1", bpm=120.0, key="8A", genre="house"),
        Track(id=2, artist="B", title="T2", bpm=121.0, key="8A", genre="house"),
        Track(id=3, artist="C", title="T3", bpm=122.0, key="9A", genre="house"),
    ]


def test_set_order_first_step_has_no_transition():
    order, transitions = build_set_order(make_chain_tracks())
    set_order = SetOrder(order, transitions)
    steps = list(set_order)
    assert steps[0].transition is None
    assert steps[0].track.id == order[0].id


def test_set_order_yields_one_step_per_track():
    order, transitions = build_set_order(make_chain_tracks())
    set_order = SetOrder(order, transitions)
    steps = list(set_order)
    assert len(steps) == len(order)
    assert [s.track.id for s in steps] == [t.id for t in order]


def test_set_order_is_a_real_iterator_supporting_next():
    order, transitions = build_set_order(make_chain_tracks())
    set_order = SetOrder(order, transitions)
    assert iter(set_order) is set_order
    first = next(set_order)
    assert isinstance(first, SetStep)


def test_set_order_raises_stop_iteration_when_exhausted():
    order, transitions = build_set_order(make_chain_tracks())
    set_order = SetOrder(order, transitions)
    for _ in order:
        next(set_order)
    with pytest.raises(StopIteration):
        next(set_order)
