import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from vinyl_set_builder.api import TrackCreate
from vinyl_set_builder.main import app


@pytest.fixture()
def client():
    # каждый тест получает свежий экземпляр репозитория (а не просто очищенный словарь), чтобы
    # тесты не утекали состоянием друг в друга, включая счётчик id
    import vinyl_set_builder.api as api_module
    from vinyl_set_builder.repository import TrackRepository

    api_module.repository = TrackRepository()
    return TestClient(app)


def test_track_create_rejects_non_positive_bpm():
    with pytest.raises(ValidationError):
        TrackCreate(artist="A", title="T1", bpm=0, key="8A")


@pytest.mark.parametrize(
    ("key", "expected_status"),
    [
        pytest.param("8A", 201, id="valid_key_creates_track"),
        pytest.param("not-a-key", 422, id="invalid_key_is_rejected"),
    ],
)
def test_create_track(client, key, expected_status):
    response = client.post(
        "/tracks",
        json={"artist": "A", "title": "T1", "bpm": 120.0, "key": key},
    )
    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.json()["id"] == 1


def test_list_tracks_returns_everything_added(client):
    client.post("/tracks", json={"artist": "A", "title": "T1", "bpm": 120.0, "key": "8A"})
    client.post("/tracks", json={"artist": "B", "title": "T2", "bpm": 121.0, "key": "8A"})
    response = client.get("/tracks")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.parametrize(
    ("track_count", "expected_status"),
    [
        pytest.param(1, 422, id="too_few_tracks"),
        pytest.param(2, 200, id="enough_tracks_returns_ordered_steps"),
    ],
)
def test_build_set(client, track_count, expected_status):
    payloads = [
        {"artist": "A", "title": "T1", "bpm": 120.0, "key": "8A"},
        {"artist": "B", "title": "T2", "bpm": 121.0, "key": "8A"},
    ]
    for payload in payloads[:track_count]:
        client.post("/tracks", json=payload)

    response = client.post("/build-set")
    assert response.status_code == expected_status
    if expected_status == 200:
        steps = response.json()["steps"]
        assert len(steps) == 2
        assert steps[0]["transition"] is None
        assert steps[1]["transition"]["is_hard_cut"] is False
