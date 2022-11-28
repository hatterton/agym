import pytest

from agym.games.breakout import BreakoutAction, BreakoutEnv, CollisionEvent
from agym.games.breakout.dtos import (
    CollisionBallPlatform,
    CollisionBallWall,
    CollisionPlatformWall,
)
from agym.games.breakout.geom import Vec2
from tests.math_utils import almost_equal_float, almost_equal_vec


@pytest.mark.breakout
@pytest.mark.collisions
@pytest.mark.ball
@pytest.mark.platform
class TestCollisionsBallPlatform:
    def test_ball_platform_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_platform_collision_level,
    ):
        level, action, ticks = ball_platform_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action.value,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, CollisionEvent)
        assert isinstance(event.collision, CollisionBallPlatform)
        assert almost_equal_vec(breakout.balls[0].velocity, Vec2(x=0, y=-1))

    def test_ball_platform_cliping_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_platform_side_collision_level,
    ):
        level, action, ticks = ball_platform_side_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action.value,
            dt=ticks,
        )

        events = breakout.pop_events()
        expected_collisions = [
            CollisionBallPlatform,
            CollisionBallWall,
            CollisionBallPlatform,
            CollisionBallWall,
            CollisionBallPlatform,
            CollisionBallWall,
        ]

        assert len(events) == len(expected_collisions)
        for expected_coll_type, event in zip(expected_collisions, events):
            assert isinstance(event, CollisionEvent)
            assert isinstance(event.collision, expected_coll_type)

    def test_ball_platform_race_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_platform_race_collision_level,
    ):
        level, action, ticks = ball_platform_race_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action.value,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, CollisionEvent)
        assert isinstance(event.collision, CollisionBallPlatform)
