from vinyl_set_builder.repository import TrackRepository


def test_add_assigns_incrementing_ids():
    repo = TrackRepository()
    first = repo.add(artist="A", title="T1", bpm=120.0, key="8A", genre="house")
    second = repo.add(artist="B", title="T2", bpm=124.0, key="9A", genre="house")
    assert first.id == 1
    assert second.id == 2


def test_list_all_returns_every_added_track():
    repo = TrackRepository()
    repo.add(artist="A", title="T1", bpm=120.0, key="8A", genre="house")
    repo.add(artist="B", title="T2", bpm=124.0, key="9A", genre="house")
    assert len(repo.list_all()) == 2


def test_get_returns_none_for_unknown_id():
    repo = TrackRepository()
    assert repo.get(999) is None


def test_get_returns_the_matching_track():
    repo = TrackRepository()
    track = repo.add(artist="A", title="T1", bpm=120.0, key="8A", genre="house")
    assert repo.get(track.id) is track
