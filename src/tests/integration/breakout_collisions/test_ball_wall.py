import pytest

from agym.games.breakout import (
    BreakoutEnv,
    Level,
    BreakoutAction,
    CollisionEvent,
)
from agym.games.breakout.collisions import (
    CollisionBallWall,
)



def test_ball_vertical_wall_left_collision_type(
    breakout: BreakoutEnv,
    ball_vertical_wall_left_collision_level,
):
    level, action, ticks = ball_vertical_wall_left_collision_level
    breakout.load_level(level)

    breakout.step(
        action=action.value,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallWall)
    assert breakout.balls[0].velocity[0] > 0
    assert breakout.balls[0].velocity[1] < 0


def test_ball_vertical_wall_right_collision_type(
    breakout: BreakoutEnv,
    ball_vertical_wall_right_collision_level,
):
    level, action, ticks = ball_vertical_wall_right_collision_level
    breakout.load_level(level)

    breakout.step(
        action=action.value,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallWall)
    assert breakout.balls[0].velocity[0] < 0
    assert breakout.balls[0].velocity[1] < 0


def test_ball_vertical_wall_top_collision_type(
    breakout: BreakoutEnv,
    ball_vertical_wall_top_collision_level,
):
    level, action, ticks = ball_vertical_wall_top_collision_level
    breakout.load_level(level)

    breakout.step(
        action=action.value,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallWall)
    assert breakout.balls[0].velocity[0] > 0
    assert breakout.balls[0].velocity[1] > 0

