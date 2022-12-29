import pytest

from agym.dtos import Size
from agym.renderers import GameMonitorRenderer


@pytest.fixture
def game_monitor_renderer(
    env_renderer, fps_label, profile_label, render_kit, config
):
    return GameMonitorRenderer(
        fps_label=fps_label,
        profile_label=profile_label,
        screen_size=config.window_screen_size,
        env_renderer=env_renderer,
        render_kit=render_kit,
    )
