import pytest

from agym.renderers import EmptyRenderer


@pytest.fixture
def empty_renderer(render_kit):
    return EmptyRenderer(render_kit)
