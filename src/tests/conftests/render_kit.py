import pytest

from agym.gui.render_kits import PygameRenderKitEngine, RenderKit


@pytest.fixture
def render_kit_engine():
    return PygameRenderKitEngine()


@pytest.fixture
def render_kit(render_kit_engine):
    return RenderKit(engine=render_kit_engine)
