import pytest

from agym.game_monitor import GameMonitor


@pytest.fixture
def game_monitor_logic(
    config,
    clock,
    log_updater,
    audio_handler,
    env,
    game_model,
):
    return GameMonitor(
        clock=clock,
        log_updater=log_updater,
        audio_handler=audio_handler,
        env=env,
        model=game_model,
        tps=config.tps,
    )
