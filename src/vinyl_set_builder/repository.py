from __future__ import annotations

from itertools import count

from vinyl_set_builder.domain.models import Track


class TrackRepository:
    """Хранилище в памяти для единственного неявного крейта. Персистентность не предусмотрена намеренно."""

    def __init__(self) -> None:
        self._tracks: dict[int, Track] = {}
        self._id_counter = count(start=1)

    def add(
        self,
        artist: str,
        title: str,
        bpm: float,
        key: str,
        genre: str,
        tags: set[str] | None = None,
    ) -> Track:
        track = Track(
            id=next(self._id_counter),
            artist=artist,
            title=title,
            bpm=bpm,
            key=key,
            genre=genre,
            tags=tags if tags is not None else set(),
        )
        self._tracks[track.id] = track
        return track

    def list_all(self) -> list[Track]:
        return list(self._tracks.values())

    def get(self, track_id: int) -> Track | None:
        return self._tracks.get(track_id)
