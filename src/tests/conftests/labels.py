import pytest

from agym.dtos import Color, Shift
from agym.gui import TextLabel


@pytest.fixture
def fps_label(init_pygame):
    return TextLabel(
        shift=Shift(x=10, y=10),
        font_size=12,
        foreground_color=Color(230, 230, 130),
        text="fps",
    )


@pytest.fixture
def profile_label(init_pygame):
    return TextLabel(
        shift=Shift(x=120, y=10),
        font_size=12,
        foreground_color=Color(180, 130, 180),
        text="profiling",
    )
