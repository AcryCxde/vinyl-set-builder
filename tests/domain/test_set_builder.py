import inspect

import pytest

from vinyl_set_builder.domain.exceptions import IncompatibleCrateError
from vinyl_set_builder.domain.models import Track
from vinyl_set_builder.domain.set_builder import (
    DEFAULT_BPM_TOLERANCE,
    SetOrder,
    SetStep,
    build_compatibility_graph,
    build_set_order,
    iter_compatible_pairs,
)


@pytest.fixture()
def graph_tracks(make_track):
    return [
        make_track(id=1, bpm=120.0, key="8A"),
        make_track(id=2, bpm=121.0, key="8A"),  # совместим с 1
        make_track(id=3, bpm=150.0, key="3B"),  # ни с кем не совместим
    ]


@pytest.fixture()
def chain_tracks(make_track):
    return [
        make_track(id=1, bpm=120.0, key="8A"),
        make_track(id=2, bpm=121.0, key="8A"),
        make_track(id=3, bpm=122.0, key="9A"),
    ]


def test_iter_compatible_pairs_is_a_generator(graph_tracks):
    assert inspect.isgenerator(iter_compatible_pairs(graph_tracks))


def test_iter_compatible_pairs_yields_only_compatible_pairs(graph_tracks):
    pairs = list(iter_compatible_pairs(graph_tracks))
    assert [(a.id, b.id) for a, b in pairs] == [(1, 2)]


@pytest.mark.parametrize(
    ("bpm_tolerance", "expected_graph"),
    [
        pytest.param(DEFAULT_BPM_TOLERANCE, {1: {2}, 2: {1}, 3: set()}, id="default_tolerance"),
        pytest.param(0.5, {1: set(), 2: set(), 3: set()}, id="tight_tolerance_breaks_the_only_pair"),
    ],
)
def test_build_compatibility_graph(graph_tracks, bpm_tolerance, expected_graph):
    graph = build_compatibility_graph(graph_tracks, bpm_tolerance=bpm_tolerance)
    assert graph == expected_graph


@pytest.mark.parametrize(
    "tracks",
    [
        pytest.param(
            [Track(id=1, artist="A", title="T1", bpm=120.0, key="8A", genre="house")],
            id="fewer_than_two_tracks",
        ),
        pytest.param(
            [
                Track(id=1, artist="A", title="T1", bpm=90.0, key="1A", genre="house"),
                Track(id=2, artist="B", title="T2", bpm=175.0, key="7B", genre="dnb"),
            ],
            id="no_compatible_pair_in_the_crate",
        ),
    ],
)
def test_build_set_order_raises(tracks):
    with pytest.raises(IncompatibleCrateError):
        build_set_order(tracks)


@pytest.mark.parametrize(
    ("third_track_key", "third_track_bpm", "expect_any_hard_cut"),
    [
        pytest.param("9A", 122.0, False, id="third_track_compatible_chain_has_no_hard_cut"),
        pytest.param("3B", 175.0, True, id="third_track_incompatible_forces_a_hard_cut"),
    ],
)
def test_build_set_order_hard_cut_depends_on_compatibility(
    make_track, third_track_key, third_track_bpm, expect_any_hard_cut
):
    tracks = [
        make_track(id=1, bpm=120.0, key="8A"),
        make_track(id=2, bpm=121.0, key="8A"),
        make_track(id=3, bpm=third_track_bpm, key=third_track_key),
    ]
    order, transitions = build_set_order(tracks)
    assert [t.id for t in order] == [1, 2, 3]
    assert any(t.is_hard_cut for t in transitions) is expect_any_hard_cut


def test_build_set_order_starts_from_the_lowest_bpm_track(make_track):
    tracks = [
        make_track(id=1, bpm=122.0, key="9A"),
        make_track(id=2, bpm=120.0, key="8A"),
        make_track(id=3, bpm=121.0, key="8A"),
    ]
    order, _ = build_set_order(tracks)
    assert order[0].id == 2


def test_set_order_iterates_all_steps_with_transitions_attached(chain_tracks):
    order, transitions = build_set_order(chain_tracks)
    set_order = SetOrder(order, transitions)

    assert iter(set_order) is set_order
    steps = list(set_order)
    assert all(isinstance(step, SetStep) for step in steps)
    assert [step.track.id for step in steps] == [1, 2, 3]
    assert steps[0].transition is None
    assert all(step.transition is not None for step in steps[1:])


def test_set_order_raises_stop_iteration_when_exhausted(make_track):
    tracks = [make_track(id=1, bpm=120.0, key="8A"), make_track(id=2, bpm=121.0, key="8A")]
    order, transitions = build_set_order(tracks)
    set_order = SetOrder(order, transitions)

    for _ in order:
        next(set_order)
    with pytest.raises(StopIteration):
        next(set_order)
