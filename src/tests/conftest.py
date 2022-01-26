import pytest

from agym.containers import create_app


@pytest.fixture
def application():
    app = create_app()
    return app


@pytest.fixture
def config(application):
    return application.config


@pytest.fixture
def game_monitor(application):
    return application.game_monitor


@pytest.fixture
def breakout(application):
    return application.breakout
