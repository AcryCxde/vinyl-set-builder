import pytest

from vinyl_set_builder.domain.models import Track
from vinyl_set_builder.domain.set_builder import SetOrder, SetStep, build_set_order


def make_tracks():
    return [
        Track(id=1, artist="A", title="T1", bpm=120.0, key="8A", genre="house"),
        Track(id=2, artist="B", title="T2", bpm=121.0, key="8A", genre="house"),
        Track(id=3, artist="C", title="T3", bpm=122.0, key="9A", genre="house"),
    ]


def test_set_order_first_step_has_no_transition():
    order, transitions = build_set_order(make_tracks())
    set_order = SetOrder(order, transitions)
    steps = list(set_order)
    assert steps[0].transition is None
    assert steps[0].track.id == order[0].id


def test_set_order_yields_one_step_per_track():
    order, transitions = build_set_order(make_tracks())
    set_order = SetOrder(order, transitions)
    steps = list(set_order)
    assert len(steps) == len(order)
    assert [s.track.id for s in steps] == [t.id for t in order]


def test_set_order_is_a_real_iterator_supporting_next():
    order, transitions = build_set_order(make_tracks())
    set_order = SetOrder(order, transitions)
    assert iter(set_order) is set_order
    first = next(set_order)
    assert isinstance(first, SetStep)


def test_set_order_raises_stop_iteration_when_exhausted():
    order, transitions = build_set_order(make_tracks())
    set_order = SetOrder(order, transitions)
    for _ in order:
        next(set_order)
    with pytest.raises(StopIteration):
        next(set_order)
