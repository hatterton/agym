import pytest

from agym.settings import Settings

from .conftests import *
from .levels import *


@pytest.fixture
def config():
    config = Settings()

    # config.breakout.env_size.x = 400
    # config.breakout.env_size.y = 400

    return config


@pytest.fixture
def env_width(config):
    return config.breakout.env_size.x


@pytest.fixture
def env_height(config):
    return config.breakout.env_size.y
