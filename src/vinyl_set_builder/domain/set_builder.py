from __future__ import annotations

from dataclasses import dataclass

from vinyl_set_builder.domain.exceptions import IncompatibleCrateError
from vinyl_set_builder.domain.graph import build_compatibility_graph
from vinyl_set_builder.domain.models import Track


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
