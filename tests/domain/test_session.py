import pytest

from vinyl_set_builder.domain.exceptions import IncompatibleCrateError
from vinyl_set_builder.domain.session import GraphBuildSession


def test_session_releases_lock_even_when_body_raises():
    with pytest.raises(ValueError):
        with GraphBuildSession():
            raise ValueError("boom")

    with GraphBuildSession() as session:
        pass
    assert session.duration_seconds is not None


def test_session_rejects_a_second_concurrent_build():
    with GraphBuildSession():
        with pytest.raises(IncompatibleCrateError):
            with GraphBuildSession():
                pass
