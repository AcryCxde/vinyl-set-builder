from vinyl_set_builder.domain.set_builder import build_set_order
from vinyl_set_builder.repository import TrackRepository
from vinyl_set_builder.seed import seed_mock_tracks


def test_seed_mock_tracks_adds_six_tracks():
    repo = TrackRepository()
    seed_mock_tracks(repo)
    assert len(repo.list_all()) == 6


def test_seed_mock_tracks_produce_a_buildable_set_with_a_hard_cut():
    repo = TrackRepository()
    seed_mock_tracks(repo)
    order, transitions = build_set_order(repo.list_all())
    assert len(order) == 6
    assert any(transition.is_hard_cut for transition in transitions)
    assert any(not transition.is_hard_cut for transition in transitions)
