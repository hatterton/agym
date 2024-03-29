import pytest

from envs.breakout import (
    BreakoutEnv,
    CollisionDetector,
    EmptyLevelBuilder,
    KDTreeCollisionDetectionEngine,
    NaiveCollisionDetectionEngine,
)


@pytest.fixture(
    params=[
        NaiveCollisionDetectionEngine(),
        KDTreeCollisionDetectionEngine(),
    ]
)
def collision_engine(request):
    return request.param


@pytest.fixture
def collision_detector(collision_engine):
    return CollisionDetector(engine=collision_engine)


@pytest.fixture
def level_builder(config):
    return EmptyLevelBuilder()


@pytest.fixture
def breakout(config, collision_detector, level_builder):
    breakout = BreakoutEnv(
        env_size=config.breakout.env_size,
        level_builder=level_builder,
        collision_detector=collision_detector,
    )
    breakout.reset()

    return breakout
