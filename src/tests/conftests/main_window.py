import pytest

from agym.main_window import MainWindow


@pytest.fixture
def main_window(
    init_io_framework,
    config,
    game_monitor_logic,
    game_monitor_renderer,
    event_source,
    render_kit,
):
    return MainWindow(
        window_size=config.window_screen_size,
        render_kit=render_kit,
        event_source=event_source,
        game_monitor=game_monitor_logic,
        game_monitor_renderer=game_monitor_renderer,
    )
