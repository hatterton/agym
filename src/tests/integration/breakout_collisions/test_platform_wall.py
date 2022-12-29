import pytest

from agym.games.breakout import (
    BreakoutAction,
    BreakoutCollisionEvent,
    BreakoutEnv,
)
from agym.games.breakout.dtos import CollisionPlatformWall
from tests.math_utils import almost_equal_float, almost_equal_vec


@pytest.mark.breakout
@pytest.mark.collisions
@pytest.mark.platform
@pytest.mark.wall
class TestCollisionsPlatformWall:
    def test_platform_left_wall_collision_type(
        self,
        breakout: BreakoutEnv,
        platform_left_wall_collision_level,
    ):
        level, action, ticks = platform_left_wall_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, BreakoutCollisionEvent)
        assert isinstance(event.collision, CollisionPlatformWall)
        assert almost_equal_float(
            event.collision.platform.rect.left, breakout.rect.left, eps=1e-3
        )

    def test_platform_right_wall_collision_type(
        self,
        breakout: BreakoutEnv,
        platform_right_wall_collision_level,
    ):
        level, action, ticks = platform_right_wall_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, BreakoutCollisionEvent)
        assert isinstance(event.collision, CollisionPlatformWall)
        assert almost_equal_float(
            event.collision.platform.rect.right, breakout.rect.right, eps=1e-3
        )
