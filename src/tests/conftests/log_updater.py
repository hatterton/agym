import pytest

from agym.updaters import (
    FPSUpdater,
    ProfileUpdater,
    ComposeUpdater,
    LimitedUpdater,
)


@pytest.fixture
def fps_updater(fps_label, fps_limiter):
    return FPSUpdater(
        label=fps_label,
        fps_limiter=fps_limiter,
    )


@pytest.fixture
def profile_updater(profile_label, time_profiler):
    return ProfileUpdater(
        label=profile_label,
        profiler=time_profiler,
    )


@pytest.fixture
def compose_updater(fps_updater, profile_updater):
    return ComposeUpdater(
        updaters=[
            fps_updater,
            profile_updater,
        ],
    )


@pytest.fixture
def log_updater(config, compose_updater):
    return LimitedUpdater(
        updater=compose_updater,
        ups=config.log_fps,
    )

