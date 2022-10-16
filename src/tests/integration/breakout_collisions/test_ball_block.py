from agym.games.breakout import (
    BreakoutEnv,
    BreakoutAction,
    CollisionEvent,
)
from agym.games.breakout.collisions import (
    CollisionBallBlock,
)
from tests.math_utils import (
    almost_equal_vec,
    almost_equal_float,
)


def test_ball_block_collision_type(
    breakout: BreakoutEnv,
    ball_block_collision_level,
):
    level, action, ticks = ball_block_collision_level
    breakout.load_level(level)

    breakout.step(
        action=action.value,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallBlock)
    assert almost_equal_vec(breakout.balls[0].velocity, [0, -1])


def test_ball_corner_block_collision_type(
    breakout: BreakoutEnv,
    ball_corner_block_collision_level,
):
    level, action, ticks = ball_corner_block_collision_level
    breakout.load_level(level)

    breakout.step(
        action=action.value,
        dt=ticks,
    )

    events = breakout.pop_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CollisionEvent)
    assert isinstance(event.collision, CollisionBallBlock)
    r2 = 2 ** 0.5
    assert almost_equal_vec(breakout.balls[0].velocity, [r2 / 2, r2 / 2])

