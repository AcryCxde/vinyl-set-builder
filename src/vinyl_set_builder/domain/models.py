import re
from dataclasses import dataclass

from vinyl_set_builder.domain.exceptions import InvalidCamelotKeyError

_CAMELOT_PATTERN = re.compile(r"^(?P<number>[1-9]|1[0-2])(?P<letter>[AB])$")


def parse_camelot_key(key: str) -> tuple[int, str]:
    """Разбирает '8A' -> (8, 'A'). Вызывает InvalidCamelotKeyError при неверном формате."""
    match = _CAMELOT_PATTERN.match(key)
    if match is None:
        raise InvalidCamelotKeyError(key)
    return int(match.group("number")), match.group("letter")


def are_keys_compatible(key_a: str, key_b: str) -> bool:
    """Правило Camelot wheel: та же тональность, параллельный мажор/минор, либо соседний номер + та же буква."""
    number_a, letter_a = parse_camelot_key(key_a)
    number_b, letter_b = parse_camelot_key(key_b)

    if number_a == number_b:
        return True  # тот же номер: идентичная тональность или параллельный мажор/минор
    if letter_a == letter_b and _numbers_adjacent(number_a, number_b):
        return True
    return False


def _numbers_adjacent(number_a: int, number_b: int) -> bool:
    diff = abs(number_a - number_b)
    return diff == 1 or diff == 11  # 11 покрывает переход по кругу 12 <-> 1


@dataclass
class Track:
    id: int
    artist: str
    title: str
    bpm: float
    key: str

    def __post_init__(self) -> None:
        parse_camelot_key(self.key)  # вызывает InvalidCamelotKeyError при неверном формате

    @property
    def coordinate(self) -> tuple[float, str]:
        """Неизменяемая пара (bpm, key), используемая для сравнения совместимости."""
        return (self.bpm, self.key)
