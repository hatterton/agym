import pytest

from timeprofiler import TimeProfiler


@pytest.fixture
def time_profiler():
    return TimeProfiler(
        window_size=10000,
        log_self=False,
    )
