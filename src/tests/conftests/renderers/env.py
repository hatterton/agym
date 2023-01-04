import pytest

from agym.env_components.breakout import BreakoutRenderer


@pytest.fixture
def env_renderer(env, render_kit, config, empty_renderer):
    return BreakoutRenderer(
        screen_size=config.env_screen_size,
        env=env,
        kdtree_renderer=empty_renderer,
        rendering_kdtree=config.rendering_kdtree,
        render_kit=render_kit,
        image_dir=config.breakout.image_dir,
    )
