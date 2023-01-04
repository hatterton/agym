import pytest

from agym.io_frameworks import RenderKit


@pytest.fixture
def render_kit_engine(io_framework_factory):
    return io_framework_factory.create_render_kit_engine()


@pytest.fixture
def render_kit(render_kit_engine):
    return RenderKit(engine=render_kit_engine)
