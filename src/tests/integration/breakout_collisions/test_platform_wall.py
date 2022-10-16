from agym.games.breakout import (
    BreakoutEnv,
    BreakoutAction,
    CollisionEvent,
)
from agym.games.breakout.collisions import (
    CollisionPlatformWall,
)
from tests.math_utils import (
    almost_equal_vec,
    almost_equal_float,
)


def test_platform_left_wall_collision_type(
    breakout: BreakoutEnv,
    platform_left_wall_collision_level,
):
    level, action, ticks = platform_left_wall_collision_level
    breakout.load_level(level)

    breakout.step(
        action=action.value,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionPlatformWall)
    assert almost_equal_float(breakout.platform.rect.left, 0, eps=1e-3)


def test_platform_right_wall_collision_type(
    breakout: BreakoutEnv,
    platform_right_wall_collision_level,
):
    level, action, ticks = platform_right_wall_collision_level
    breakout.load_level(level)

    breakout.step(
        action=action.value,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionPlatformWall)
    assert almost_equal_float(breakout.platform.rect.right, breakout.env_width, eps=1e-3)
