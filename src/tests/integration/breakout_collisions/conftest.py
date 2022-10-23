import pytest

from agym.games.breakout import (
    BreakoutEnv,
)


@pytest.fixture
def breakout(env_width, env_height):
    breakout = BreakoutEnv(
        env_width=env_width,
        env_height=env_height,
        check_gameover=False,
    )
    breakout.reset()

    return breakout


