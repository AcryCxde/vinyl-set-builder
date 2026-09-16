import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from vinyl_set_builder.api import TrackCreate
from vinyl_set_builder.main import app


def make_client():
    # каждый тест получает свежий экземпляр репозитория (а не просто очищенный словарь), чтобы
    # тесты не утекали состоянием друг в друга, включая счётчик id
    from vinyl_set_builder import api
    from vinyl_set_builder.repository import TrackRepository

    api.repository = TrackRepository()
    return TestClient(app)


def test_track_create_accepts_valid_payload():
    payload = TrackCreate(artist="A", title="T1", bpm=120.0, key="8A", genre="house", tags={"dark"})
    assert payload.tags == {"dark"}


def test_track_create_defaults_tags_to_empty_set():
    payload = TrackCreate(artist="A", title="T1", bpm=120.0, key="8A", genre="house")
    assert payload.tags == set()


def test_track_create_rejects_non_positive_bpm():
    with pytest.raises(ValidationError):
        TrackCreate(artist="A", title="T1", bpm=0, key="8A", genre="house")


def test_create_track_returns_201_with_assigned_id():
    client = make_client()
    response = client.post(
        "/tracks",
        json={"artist": "A", "title": "T1", "bpm": 120.0, "key": "8A", "genre": "house"},
    )
    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_create_track_rejects_invalid_camelot_key():
    client = make_client()
    response = client.post(
        "/tracks",
        json={"artist": "A", "title": "T1", "bpm": 120.0, "key": "not-a-key", "genre": "house"},
    )
    assert response.status_code == 422


def test_list_tracks_returns_everything_added():
    client = make_client()
    client.post("/tracks", json={"artist": "A", "title": "T1", "bpm": 120.0, "key": "8A", "genre": "house"})
    client.post("/tracks", json={"artist": "B", "title": "T2", "bpm": 121.0, "key": "8A", "genre": "house"})
    response = client.get("/tracks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_build_set_returns_ordered_steps():
    client = make_client()
    client.post("/tracks", json={"artist": "A", "title": "T1", "bpm": 120.0, "key": "8A", "genre": "house"})
    client.post("/tracks", json={"artist": "B", "title": "T2", "bpm": 121.0, "key": "8A", "genre": "house"})
    response = client.post("/build-set")
    assert response.status_code == 200
    steps = response.json()["steps"]
    assert len(steps) == 2
    assert steps[0]["transition"] is None
    assert steps[1]["transition"]["is_hard_cut"] is False


def test_build_set_returns_422_when_crate_too_small():
    client = make_client()
    client.post("/tracks", json={"artist": "A", "title": "T1", "bpm": 120.0, "key": "8A", "genre": "house"})
    response = client.post("/build-set")
    assert response.status_code == 422
