import pytest

from agym.game_monitor import GameMonitor


@pytest.fixture
def game_monitor(
    config,
    fps_limiter,
    fps_label,
    profile_label,
    log_updater,
    audio_handler,
    env,
    game_model,
    time_profiler,
):
    return GameMonitor(
        width=config.window_screen_width,
        height=config.window_screen_width,
        fps_limiter=fps_limiter,
        fps_label=fps_label,
        profile_label=profile_label,
        log_updater=log_updater,
        audio_handler=audio_handler,
        env=env,
        model=game_model,
        time_profiler=time_profiler,
        tps=config.tps,
    )
