import pytest

from agym.games.breakout import BreakoutEnv


@pytest.fixture
def breakout(config, collision_detector, level_builder):
    breakout = BreakoutEnv(
        env_size=config.breakout.env_size,
        level_builder=level_builder,
        collision_detector=collision_detector,
        checking_gameover=False,
    )
    breakout.reset()

    return breakout
