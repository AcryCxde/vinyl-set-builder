import pytest

from vinyl_set_builder.domain.exceptions import IncompatibleCrateError
from vinyl_set_builder.domain.session import GraphBuildSession


def test_session_records_a_nonnegative_duration():
    with GraphBuildSession() as session:
        pass
    assert session.duration_seconds is not None
    assert session.duration_seconds >= 0


def test_session_releases_lock_after_normal_exit():
    with GraphBuildSession():
        pass
    # сразу после этого должна суметь начаться вторая сессия
    with GraphBuildSession():
        pass


def test_session_releases_lock_even_when_body_raises():
    with pytest.raises(ValueError):
        with GraphBuildSession():
            raise ValueError("boom")
    # блокировка должна быть снята, несмотря на исключение
    with GraphBuildSession():
        pass


def test_session_raises_if_a_build_is_already_in_progress():
    with GraphBuildSession():
        with pytest.raises(IncompatibleCrateError):
            with GraphBuildSession():
                pass
