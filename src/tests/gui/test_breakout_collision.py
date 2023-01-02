import pytest

from agym.games.breakout import BreakoutEnv, KDTreeCollisionDetectionEngine
from agym.main_window import MainWindow
from agym.protocols import IEventSource

from .game_model import DummyModel
from .gui_test_runner import GUITestRunner


@pytest.fixture
def collision_engine():
    return KDTreeCollisionDetectionEngine()


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


@pytest.fixture
def env(breakout):
    return breakout


@pytest.fixture
def game_model() -> DummyModel:
    return DummyModel()


@pytest.fixture
def test_runner(
    main_window: MainWindow,
    breakout: BreakoutEnv,
    game_model: DummyModel,
    event_source: IEventSource,
):
    return GUITestRunner(
        window=main_window,
        env=breakout,
        event_source=event_source,
        model=game_model,
    )


@pytest.mark.gui
@pytest.mark.breakout
def test_gui(
    test_runner,
    all_levels,
):
    test_runner.run(all_levels)
