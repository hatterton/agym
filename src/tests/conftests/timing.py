import pytest

from agym.utils import TimeProfiler


@pytest.fixture
def time_profiler(config):
    return TimeProfiler(
        window_size=10000,
        log_self=False,
    )
