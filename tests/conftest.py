from collections.abc import Callable

import pytest

from vinyl_set_builder.domain.models import Track


@pytest.fixture()
def make_track() -> Callable[..., Track]:
    def _make(
        id: int = 1,
        artist: str = "DJ Shadow",
        title: str = "Building Steam",
        bpm: float = 91.0,
        key: str = "8A",
    ) -> Track:
        return Track(id=id, artist=artist, title=title, bpm=bpm, key=key)

    return _make
