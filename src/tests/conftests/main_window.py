import pytest

from agym.main_window import MainWindow


@pytest.fixture
def main_window(init_pygame, config, game_monitor):
    return MainWindow(
        width=config.window_screen_width,
        height=config.window_screen_height,
        game_monitor=game_monitor,
    )
