from agym.games.breakout import (
    BreakoutEnv,
    BreakoutAction,
    CollisionEvent,
)
from agym.games.breakout.collisions import (
    CollisionBallPlatform,
    CollisionBallWall,
    CollisionPlatformWall,
)
from tests.math_utils import (
    almost_equal_vec,
    almost_equal_float,
)



def test_ball_platform_collision_type(
    breakout: BreakoutEnv,
    ball_platform_collision_level,
):
    level, action, ticks = ball_platform_collision_level
    breakout.load_level(level)

    breakout.step(
        action=action.value,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallPlatform)
    assert almost_equal_vec(breakout.balls[0].velocity, [0, -1])


def test_ball_platform_cliping_collision_type(
    breakout: BreakoutEnv,
    ball_platform_side_collision_level,
):
    level, action, ticks = ball_platform_side_collision_level
    breakout.load_level(level)

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
    breakout: BreakoutEnv,
    ball_platform_race_collision_level,
):
    level, action, ticks = ball_platform_race_collision_level
    breakout.load_level(level)

    breakout.step(
        action=action.value,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallPlatform)
