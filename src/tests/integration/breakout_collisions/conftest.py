import pytest

from agym.games.breakout import (
    BreakoutEnv,
)


@pytest.fixture
def breakout():
    breakout = BreakoutEnv(
        env_width=450,
        env_height=500,
    )
    breakout.reset()

    return breakout


