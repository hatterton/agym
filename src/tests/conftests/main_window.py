import pytest

from agym.dtos import Size
from agym.main_window import MainWindow


@pytest.fixture
def main_window(init_pygame, config, game_monitor, render_kit):
    return MainWindow(
        window_size=Size(
            width=config.window_screen_width,
            height=config.window_screen_height,
        ),
        render_kit=render_kit,
        game_monitor=game_monitor,
    )
