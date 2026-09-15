from collections.abc import Iterator

from vinyl_set_builder.domain.camelot import are_keys_compatible
from vinyl_set_builder.domain.models import Track

DEFAULT_BPM_TOLERANCE = 6.0


def iter_compatible_pairs(
    tracks: list[Track], bpm_tolerance: float = DEFAULT_BPM_TOLERANCE
) -> Iterator[tuple[Track, Track]]:
    """Лениво выдаёт совместимые пары треков, не материализуя все C(n,2) пар сразу."""
    for i, track_a in enumerate(tracks):
        for track_b in tracks[i + 1 :]:
            if abs(track_a.bpm - track_b.bpm) <= bpm_tolerance and are_keys_compatible(
                track_a.key, track_b.key
            ):
                yield track_a, track_b


def build_compatibility_graph(
    tracks: list[Track], bpm_tolerance: float = DEFAULT_BPM_TOLERANCE
) -> dict[int, set[int]]:
    """Граф смежности через множества: track_id -> множество id совместимых соседей."""
    graph: dict[int, set[int]] = {track.id: set() for track in tracks}
    for track_a, track_b in iter_compatible_pairs(tracks, bpm_tolerance):
        graph[track_a.id].add(track_b.id)
        graph[track_b.id].add(track_a.id)
    return graph
