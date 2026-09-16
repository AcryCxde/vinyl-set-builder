from vinyl_set_builder.repository import TrackRepository


def seed_mock_tracks(repository: TrackRepository) -> None:
    """Заполняет репозиторий демонстрационным крейтом современного хип-хопа, чтобы сразу после
    запуска можно было вызвать /build-set, не добавляя треки вручную через Swagger.

    Треки подобраны специально: первые пять образуют плавную цепочку по темпу и тональности,
    а последний (HUMBLE.) намеренно выбивается из неё — это гарантирует, что при построении
    сета будет виден и обычный переход, и жёсткий обрыв (hard cut)."""
    repository.add(artist="Tyler, The Creator", title="See You Again", bpm=70.0, key="7A")
    repository.add(artist="Tyler, The Creator", title="EARFQUAKE", bpm=75.0, key="8A")
    repository.add(artist="Post Malone", title="Sunflower", bpm=81.0, key="8A")
    repository.add(artist="Post Malone", title="rockstar", bpm=87.0, key="9A")
    repository.add(artist="Kendrick Lamar", title="LOVE.", bpm=93.0, key="9B")
    repository.add(artist="Kendrick Lamar", title="HUMBLE.", bpm=150.0, key="3B")
