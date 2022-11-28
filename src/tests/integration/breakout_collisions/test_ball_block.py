import pytest

from agym.games.breakout import BreakoutAction, BreakoutEnv, CollisionEvent
from agym.games.breakout.dtos import CollisionBallBlock
from agym.games.breakout.geom import Vec2
from tests.math_utils import almost_equal_float, almost_equal_vec


@pytest.mark.breakout
@pytest.mark.collisions
@pytest.mark.ball
@pytest.mark.block
class TestCollisionsBallBlock:
    def test_ball_block_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_block_collision_level,
    ):
        level, action, ticks = ball_block_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action.value,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, CollisionEvent)
        assert isinstance(event.collision, CollisionBallBlock)
        assert almost_equal_vec(breakout.balls[0].velocity, Vec2(x=0, y=-1))

    def test_ball_corner_block_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_corner_block_collision_level,
    ):
        level, action, ticks = ball_corner_block_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action.value,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, CollisionEvent)
        assert isinstance(event.collision, CollisionBallBlock)
        r2 = 2**0.5
        assert almost_equal_vec(
            breakout.balls[0].velocity, Vec2(x=r2 / 2, y=r2 / 2)
        )
