import pytest

from vinyl_set_builder.domain.exceptions import IncompatibleCrateError
from vinyl_set_builder.domain.set_builder import SetOrder, build_compatibility_graph, build_set_order


def test_build_compatibility_graph_links_only_compatible_tracks(make_track):
    tracks = [
        make_track(id=1, bpm=120.0, key="8A"),
        make_track(id=2, bpm=121.0, key="8A"),
        make_track(id=3, bpm=150.0, key="3B"),
    ]
    assert build_compatibility_graph(tracks) == {1: {2}, 2: {1}, 3: set()}


@pytest.mark.parametrize(
    "specs",
    [
        pytest.param([(120.0, "8A")], id="fewer_than_two_tracks"),
        pytest.param([(90.0, "1A"), (175.0, "7B")], id="no_compatible_pair"),
    ],
)
def test_build_set_order_raises_for_unbuildable_crate(make_track, specs):
    tracks = [make_track(id=i, bpm=bpm, key=key) for i, (bpm, key) in enumerate(specs, start=1)]
    with pytest.raises(IncompatibleCrateError):
        build_set_order(tracks)


def test_build_set_order_starts_lowest_bpm_and_follows_closest_compatible_track(make_track):
    tracks = [
        make_track(id=1, bpm=122.0, key="9A"),
        make_track(id=2, bpm=120.0, key="8A"),
        make_track(id=3, bpm=124.0, key="8A"),
    ]
    order, transitions = build_set_order(tracks)
    assert [t.id for t in order] == [2, 1, 3]
    assert not any(t.is_hard_cut for t in transitions)


def test_build_set_order_marks_hard_cut_when_no_compatible_track_is_left(make_track):
    tracks = [
        make_track(id=1, bpm=120.0, key="8A"),
        make_track(id=2, bpm=121.0, key="8A"),
        make_track(id=3, bpm=175.0, key="3B"),
    ]
    order, transitions = build_set_order(tracks)
    assert [t.id for t in order] == [1, 2, 3]
    assert [t.is_hard_cut for t in transitions] == [False, True]


def test_set_order_yields_first_step_without_transition_then_stops(make_track):
    tracks = [make_track(id=1, bpm=120.0, key="8A"), make_track(id=2, bpm=121.0, key="8A")]
    set_order = SetOrder(*build_set_order(tracks))

    steps = list(set_order)

    assert [step.track.id for step in steps] == [1, 2]
    assert steps[0].transition is None
    assert steps[1].transition is not None
    with pytest.raises(StopIteration):
        next(set_order)
