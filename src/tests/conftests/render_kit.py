import pytest

from agym.gui.render_kits import PygameRenderKit


@pytest.fixture
def render_kit():
    return PygameRenderKit()
