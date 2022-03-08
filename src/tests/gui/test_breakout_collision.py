import pytest
from typing import cast
from time import sleep
from threading import Thread, Timer

from agym.main_window import (
    MainWindow,
)
from agym.games.breakout import (
    BreakoutEnv,
)


def run_gui_test(main_window: MainWindow, t: float) -> None:
    t1 = Thread(target=main_window.run)
    t2 = Timer(t, main_window.deactivate)

    t1.start()
    t2.start()

    t1.join()
    t2.cancel()


@pytest.fixture
def main_window(main_window) -> MainWindow:
    return main_window()


TICKS_PER_SECOND = 20

def test_gui(
    main_window: MainWindow,
    breakout: BreakoutEnv,
    all_levels,
):
    for test_case in all_levels:
        level, ticks = test_case

        breakout.reset()
        breakout.load_level(level)

        run_gui_test(
            main_window=main_window,
            t=ticks / TICKS_PER_SECOND,
        )
