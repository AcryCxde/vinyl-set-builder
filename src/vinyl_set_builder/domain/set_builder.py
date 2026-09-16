from collections.abc import Iterator
from dataclasses import dataclass

from vinyl_set_builder.domain.exceptions import IncompatibleCrateError
from vinyl_set_builder.domain.models import Track, are_keys_compatible

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


@dataclass(frozen=True)
class Transition:
    from_track: Track
    to_track: Track
    is_hard_cut: bool


def build_set_order(tracks: list[Track]) -> tuple[list[Track], list[Transition]]:
    """Жадно упорядочивает треки по разнице BPM, начиная с самого медленного трека. Вызывает
    IncompatibleCrateError, если крейт слишком мал или в нём вообще нет совместимой пары."""
    if len(tracks) < 2:
        raise IncompatibleCrateError("В крейте должно быть минимум 2 трека, чтобы построить сет")

    by_id = {track.id: track for track in tracks}
    graph = build_compatibility_graph(tracks)
    if not any(graph.values()):
        raise IncompatibleCrateError("В крейте не нашлось ни одной совместимой пары треков")

    current_id = min(tracks, key=lambda t: t.bpm).id
    visited = {current_id}
    order = [by_id[current_id]]
    transitions: list[Transition] = []

    while len(visited) < len(tracks):
        current = by_id[current_id]
        candidates = [tid for tid in graph[current_id] if tid not in visited]
        is_hard_cut = not candidates
        pool = candidates if candidates else [tid for tid in by_id if tid not in visited]

        next_id = min(pool, key=lambda tid: abs(current.bpm - by_id[tid].bpm))
        next_track = by_id[next_id]
        transitions.append(Transition(from_track=current, to_track=next_track, is_hard_cut=is_hard_cut))

        order.append(next_track)
        visited.add(next_id)
        current_id = next_id

    return order, transitions


@dataclass(frozen=True)
class SetStep:
    track: Track
    transition: Transition | None  # None только для самого первого трека


class SetOrder:
    """Собственный итератор по построенному сету: отдаёт пары (трек, входящий переход)."""

    def __init__(self, order: list[Track], transitions: list[Transition]) -> None:
        self._steps: list[SetStep] = [SetStep(order[0], None)] + [
            SetStep(transition.to_track, transition) for transition in transitions
        ]
        self._index = 0

    def __iter__(self) -> Iterator[SetStep]:
        return self

    def __next__(self) -> SetStep:
        if self._index >= len(self._steps):
            raise StopIteration
        step = self._steps[self._index]
        self._index += 1
        return step
