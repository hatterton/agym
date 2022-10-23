import pytest

from agym.gui import TextLabel


@pytest.fixture
def fps_label(init_pygame):
    return TextLabel(
        x=10,
        y=10,
        font_size=12,
        text="fps",
    )


@pytest.fixture
def profile_label(init_pygame):
    return TextLabel(
        x=120,
        y=10,
        font_size=12,
        color=(180, 130, 180),
        text="profiling",
    )
