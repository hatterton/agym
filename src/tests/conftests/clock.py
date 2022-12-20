import pytest

from agym.clocks import FramerateClockDecorator, PygameClock


@pytest.fixture
def clock(config):
    pygame_clock = PygameClock(
        target_framerate=config.graphics_framerate,
    )

    clock = FramerateClockDecorator(
        clock=pygame_clock,
        history_size=config.framerate_history_size,
    )

    return clock
