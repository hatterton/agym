import pytest

from agym.main_window import (
    MainWindow,
)
from tests.gui.game_model import DummyModel


@pytest.fixture
def main_window(main_window) -> MainWindow:
    return main_window()


@pytest.fixture
def game_model(game_monitor) -> DummyModel:
    model = DummyModel()
    game_monitor().model = model

    return model

