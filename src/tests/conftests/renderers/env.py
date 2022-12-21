import pytest

from agym.dtos import Size
from agym.renderers import EnvRenderer


@pytest.fixture
def env_renderer(env, render_kit, config, empty_renderer):
    return EnvRenderer(
        screen_size=Size(width=config.env_width, height=config.env_height),
        env=env,
        kdtree_renderer=empty_renderer,
        render_kit=render_kit,
        image_dir=config.breakout.image_dir,
    )
