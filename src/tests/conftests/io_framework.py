import pytest

from agym.io_frameworks import PygameIOFrameworkFactory


@pytest.fixture
def io_framework_factory():
    return PygameIOFrameworkFactory()


@pytest.fixture
def init_io_framework(io_framework_factory):
    io_framework_factory.init_framework()
