from vinyl_set_builder.repository import TrackRepository


def test_add_assigns_incrementing_ids_and_list_all_returns_tracks_in_insertion_order():
    repo = TrackRepository()
    first = repo.add(artist="A", title="T1", bpm=120.0, key="8A")
    second = repo.add(artist="B", title="T2", bpm=124.0, key="9A")

    assert (first.id, second.id) == (1, 2)
    assert repo.list_all() == [first, second]
