from __future__ import annotations


class VinylSetBuilderError(Exception):
    """Базовый класс для всех доменных ошибок vinyl_set_builder."""


class InvalidCamelotKeyError(VinylSetBuilderError):
    """Вызывается, если строка не соответствует нотации Camelot wheel (например, '8A')."""

    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"'{key}' не является допустимой Camelot-тональностью (ожидается, например, '8A', '12B')")


class IncompatibleCrateError(VinylSetBuilderError):
    """Вызывается, если из текущего крейта невозможно построить порядок сета."""
