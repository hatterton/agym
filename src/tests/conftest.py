import pytest

from agym.containers import create_app
from .testing_levels import *


@pytest.fixture
def application():
    app = create_app()
    return app


@pytest.fixture
def config(application):
    return application.config


@pytest.fixture
def main_window(application):
    return application.main_window


@pytest.fixture
def game_monitor(application):
    return application.game_monitor


@pytest.fixture
def breakout(game_monitor):
    return game_monitor().env
