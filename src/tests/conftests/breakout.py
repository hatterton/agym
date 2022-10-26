import pytest

from agym.games.breakout import (
    BreakoutEnv,
    LegacyCollisionDetectorEngine,
    KDTreeCollisionDetectorEngine,
    CollisionDetector,
    DefaultLevelBuilder,
)

@pytest.fixture
def collision_engine():
    # return LegacyCollisionDetectorEngine()
    return KDTreeCollisionDetectorEngine()


@pytest.fixture
def collision_detector(collision_engine):
    return CollisionDetector(engine=collision_engine)


@pytest.fixture
def level_builder(config):
    return DefaultLevelBuilder(
        env_width=config.env_width,
        env_height=config.env_height,
        ball_speed=config.ball_speed,
        platform_speed=config.platform_speed,
    )


@pytest.fixture
def breakout(config, collision_detector, level_builder):
    breakout = BreakoutEnv(
        env_width=config.env_width,
        env_height=config.env_height,
        level_builder=level_builder,
        collision_detector=collision_detector,
    )
    breakout.reset()

    return breakout
