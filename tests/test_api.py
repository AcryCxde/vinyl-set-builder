import pytest
from fastapi.testclient import TestClient

from vinyl_set_builder.main import app

TRACK_A = {"artist": "A", "title": "T1", "bpm": 120.0, "key": "8A"}
TRACK_B = {"artist": "B", "title": "T2", "bpm": 121.0, "key": "8A"}


@pytest.fixture()
def client():
    # свежий репозиторий на каждый тест, включая счётчик id
    import vinyl_set_builder.api as api_module
    from vinyl_set_builder.repository import TrackRepository

    api_module.repository = TrackRepository()
    return TestClient(app)


@pytest.mark.parametrize(
    ("key", "expected_status"),
    [
        pytest.param("8A", 201, id="valid_key_creates_track"),
        pytest.param("not-a-key", 422, id="invalid_key_is_rejected"),
    ],
)
def test_create_track(client, key, expected_status):
    response = client.post("/tracks", json={**TRACK_A, "key": key})
    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.json()["id"] == 1


def test_list_tracks_returns_everything_added(client):
    client.post("/tracks", json=TRACK_A)
    client.post("/tracks", json=TRACK_B)
    response = client.get("/tracks")
    assert response.status_code == 200
    assert [track["title"] for track in response.json()] == ["T1", "T2"]


@pytest.mark.parametrize(
    ("payloads", "expected_status"),
    [
        pytest.param([TRACK_A], 422, id="too_few_tracks"),
        pytest.param([TRACK_A, TRACK_B], 200, id="enough_tracks_returns_ordered_steps"),
    ],
)
def test_build_set(client, payloads, expected_status):
    for payload in payloads:
        client.post("/tracks", json=payload)

    response = client.post("/build-set")

    assert response.status_code == expected_status
    if expected_status == 200:
        steps = response.json()["steps"]
        assert steps[0]["transition"] is None
        assert steps[1]["transition"] == {"to_track_id": 2, "is_hard_cut": False}
