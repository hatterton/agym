import pytest


@pytest.fixture
def game_monitor(game_monitor):
    return game_monitor()


def test_game_monitor__inited(game_monitor):
    pass

