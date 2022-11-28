import pytest

from agym.games.breakout import BreakoutEnv
from agym.main_window import MainWindow
from tests.gui.game_model import DummyModel


@pytest.fixture
def env(config, collision_detector, level_builder):
    breakout = BreakoutEnv(
        env_width=config.env_width,
        env_height=config.env_height,
        level_builder=level_builder,
        collision_detector=collision_detector,
        checking_gameover=False,
    )
    breakout.reset()

    return breakout


@pytest.fixture
def game_model() -> DummyModel:
    return DummyModel()
