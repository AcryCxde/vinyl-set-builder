import time
from types import TracebackType


class BuildTimer:
    """Замеряет время выполнения блока `with`, в том числе если внутри бросили исключение."""

    def __init__(self) -> None:
        self.duration_seconds = 0.0
        self._start = 0.0

    def __enter__(self) -> "BuildTimer":
        self._start = time.monotonic()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.duration_seconds = time.monotonic() - self._start
