import pytest

from agym.dtos import Color
from agym.renderers import TextLabel


@pytest.fixture
def fps_label(init_io_framework, render_kit):
    return TextLabel(
        render_kit=render_kit,
        font=render_kit.create_font("Hack", 12),
        foreground_color=Color(230, 230, 130),
        text="fps",
    )


@pytest.fixture
def profile_label(init_io_framework, render_kit):
    return TextLabel(
        render_kit=render_kit,
        font=render_kit.create_font("Hack", 12),
        foreground_color=Color(180, 130, 180),
        text="profiling",
    )
