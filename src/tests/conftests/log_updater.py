import pytest

from agym.updaters import (
    ComposeUpdater,
    FPSUpdater,
    LimitedUpdater,
    ProfileUpdater,
)


@pytest.fixture
def fps_updater(fps_label, clock):
    return FPSUpdater(
        label=fps_label,
        clock=clock,
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
def log_updater(config, clock, compose_updater):
    return LimitedUpdater(
        updater=compose_updater,
        clock=clock,
        ups=config.log_framerate,
    )
