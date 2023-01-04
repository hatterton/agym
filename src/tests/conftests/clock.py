import pytest

from agym.io_frameworks import FramerateClockDecorator


@pytest.fixture
def clock(io_framework_factory, config):
    clock = io_framework_factory.create_clock(
        target_framerate=config.graphics_framerate,
    )

    clock = FramerateClockDecorator(
        clock=clock,
        history_size=config.framerate_history_size,
    )

    return clock
