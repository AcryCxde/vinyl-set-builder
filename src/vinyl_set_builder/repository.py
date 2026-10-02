from itertools import count

from vinyl_set_builder.domain.models import Track


class TrackRepository:
    """Хранилище треков в памяти."""

    def __init__(self) -> None:
        self._tracks: dict[int, Track] = {}
        self._id_counter = count(start=1)

    def add(
        self,
        artist: str,
        title: str,
        bpm: float,
        key: str,
    ) -> Track:
        track = Track(
            id=next(self._id_counter),
            artist=artist,
            title=title,
            bpm=bpm,
            key=key,
        )
        self._tracks[track.id] = track
        return track

    def list_all(self) -> list[Track]:
        return list(self._tracks.values())
