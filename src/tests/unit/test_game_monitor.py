import pytest


@pytest.fixture
def game_monitor(game_monitor):
    return game_monitor()


# def test_game_monitor__deactivating(game_monitor):
#     assert not game_monitor.is_active

#     game_monitor.is_active = True
#     assert game_monitor.is_active

#     game_monitor.deactive()
#     assert not game_monitor.is_active


# def test_game_monitor__setting_game(game_monitor):
#     env = "Some env"

#     assert game_monitor.env != env

#     game_monitor.set_game(env)
#     assert game_monitor.env == env
