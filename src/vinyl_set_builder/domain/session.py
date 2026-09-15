import time
from types import TracebackType

from vinyl_set_builder.domain.exceptions import IncompatibleCrateError


class GraphBuildSession:
    """Оберегает построение графа совместимости: блокирует (единственный) крейт от
    одновременных построений и замеряет время построения, снимая блокировку даже при ошибке."""

    _locked: bool = False

    def __init__(self) -> None:
        self.duration_seconds: float | None = None
        self._start_time: float | None = None

    def __enter__(self) -> "GraphBuildSession":
        if GraphBuildSession._locked:
            raise IncompatibleCrateError("Для этого крейта уже строится сет")
        GraphBuildSession._locked = True
        self._start_time = time.monotonic()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        assert self._start_time is not None
        self.duration_seconds = time.monotonic() - self._start_time
        GraphBuildSession._locked = False
        # возврат None (ложное значение) никогда не подавляет исключения
