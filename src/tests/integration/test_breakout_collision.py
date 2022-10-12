import pytest
from typing import cast, List

from agym.games.breakout import (
    ItemManager,
    BreakoutEnv,
    Level,
    BreakoutAction,
    CollisionEvent,
)
from agym.games.breakout.collisions import (
    CollisionBallBlock,
    CollisionBallPlatform,
    CollisionBallWall,
    CollisionPlatformWall,
)

@pytest.fixture
def breakout():
    breakout = BreakoutEnv(
        env_width=450,
        env_height=500,
    )
    breakout.reset()

    return breakout


def almost_equal_float(a: float, b: float, eps: float = 1e-4) -> bool:
    return abs(a - b) < eps


Vec = List[float]
def almost_equal_vec(a: Vec, b: Vec) -> bool:
    return (
        almost_equal_float(a[0], b[0]) and
        almost_equal_float(a[1], b[1])
    )


def test_ball_block_collision_type(
    breakout: BreakoutEnv,
    ball_block_collision_level,
):
    level, ticks = ball_block_collision_level
    breakout.load_level(level)

    breakout.step(
        action=0,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallBlock)
    assert almost_equal_vec(breakout.ball.vec_velocity, [0, -1])


def test_ball_corner_block_collision_type(
    breakout: BreakoutEnv,
    ball_corner_block_collision_level,
):
    level, ticks = ball_corner_block_collision_level
    breakout.load_level(level)

    breakout.step(
        action=0,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallBlock)
    r2 = 2 ** 0.5
    assert almost_equal_vec(breakout.ball.vec_velocity, [r2 / 2, r2 / 2])


def test_ball_vertical_wall_left_collision_type(
    breakout: BreakoutEnv,
    ball_vertical_wall_left_collision_level,
):
    level, ticks = ball_vertical_wall_left_collision_level
    breakout.load_level(level)

    breakout.step(
        action=0,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallWall)
    assert breakout.ball.vec_velocity[0] > 0
    assert breakout.ball.vec_velocity[1] < 0


def test_ball_vertical_wall_right_collision_type(
    breakout: BreakoutEnv,
    ball_vertical_wall_right_collision_level,
):
    level, ticks = ball_vertical_wall_right_collision_level
    breakout.load_level(level)

    breakout.step(
        action=0,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallWall)
    assert breakout.ball.vec_velocity[0] < 0
    assert breakout.ball.vec_velocity[1] < 0


def test_ball_vertical_wall_top_collision_type(
    breakout: BreakoutEnv,
    ball_vertical_wall_top_collision_level,
):
    level, ticks = ball_vertical_wall_top_collision_level
    breakout.load_level(level)

    breakout.step(
        action=0,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallWall)
    assert breakout.ball.vec_velocity[0] > 0
    assert breakout.ball.vec_velocity[1] > 0
