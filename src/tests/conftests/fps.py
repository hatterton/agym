import pytest

from agym.utils import FPSLimiter


@pytest.fixture
def fps_limiter(config):
    return FPSLimiter(
        max_fps=config.max_fps,
        history_size=1000,
    )
