import inspect

from vinyl_set_builder.domain.graph import build_compatibility_graph, iter_compatible_pairs
from vinyl_set_builder.domain.models import Track


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
