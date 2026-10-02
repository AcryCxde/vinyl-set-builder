from vinyl_set_builder.domain.set_builder import build_set_order
from vinyl_set_builder.repository import TrackRepository
from vinyl_set_builder.seed import seed_mock_tracks


def test_seeded_crate_builds_a_set_that_is_reordered_and_ends_with_a_hard_cut():
    repo = TrackRepository()
    seed_mock_tracks(repo)
    tracks = repo.list_all()

    order, transitions = build_set_order(tracks)

    assert [t.bpm for t in order] == sorted(t.bpm for t in tracks)
    assert [t.id for t in order] != [t.id for t in tracks]
    assert [t.is_hard_cut for t in transitions] == [False] * 4 + [True]
