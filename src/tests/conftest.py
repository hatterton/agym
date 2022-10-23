import pytest

from agym.settings import Settings

from .levels import *
from .conftests import *


@pytest.fixture
def config():
    return Settings()

@pytest.fixture
def env_width(config):
    return config.env_width

@pytest.fixture
def env_height(config):
    return config.env_height
