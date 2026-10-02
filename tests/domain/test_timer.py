import pytest

from vinyl_set_builder.domain.timer import BuildTimer


def test_timer_records_duration_even_when_body_raises():
    timer = BuildTimer()
    with pytest.raises(ValueError):
        with timer:
            raise ValueError("boom")

    assert timer.duration_seconds > 0
