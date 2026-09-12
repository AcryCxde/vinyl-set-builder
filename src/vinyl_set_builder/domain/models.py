from __future__ import annotations

from dataclasses import dataclass, field

from vinyl_set_builder.domain.camelot import parse_camelot_key


@dataclass
class Track:
    id: int
    artist: str
    title: str
    bpm: float
    key: str
    genre: str
    tags: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        parse_camelot_key(self.key)  # вызывает InvalidCamelotKeyError при неверном формате

    @property
    def coordinate(self) -> tuple[float, str]:
        """Неизменяемая пара (bpm, key), используемая для сравнения совместимости."""
        return (self.bpm, self.key)
