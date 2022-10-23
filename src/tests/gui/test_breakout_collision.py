import pytest
from threading import Thread, Timer

from agym.main_window import (
    MainWindow,
)
from agym.games.breakout import (
    BreakoutEnv,
)

from tests.gui.game_model import DummyModel


@pytest.fixture
def breakout(env):
    return env


def run_gui_test(main_window: MainWindow, t: float) -> None:
    t1 = Thread(target=main_window.run)
    t2 = Timer(t, main_window.deactivate)

    t1.start()
    t2.start()

    t1.join()
    t2.cancel()


TICKS_PER_SECOND = 20


def test_gui(
    main_window: MainWindow,
    breakout: BreakoutEnv,
    game_model: DummyModel,
    all_levels,
):
    for test_case in all_levels:
        level, action, ticks = test_case

        breakout.reset()
        breakout.load_level(level)

        game_model.set_action(action)

        run_gui_test(
            main_window=main_window,
            t=ticks / TICKS_PER_SECOND,
        )
