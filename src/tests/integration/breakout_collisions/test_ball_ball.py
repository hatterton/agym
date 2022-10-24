import pytest

from agym.games.breakout import (
    BreakoutEnv,
    BreakoutAction,
    CollisionEvent,
)
from agym.games.breakout.geom import (
    Vec2,
)
from agym.games.breakout.collisions import (
    CollisionBallBall,
)
from tests.math_utils import (
    almost_equal_vec,
    almost_equal_float,
)


@pytest.mark.breakout
@pytest.mark.collisions
@pytest.mark.ball
class TestCollisionsBallBall:
    def test_ball_ball_central_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_ball_moving_stop_collision_level,
    ):
        level, action, ticks = ball_ball_moving_stop_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action.value,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, CollisionEvent)
        assert isinstance(event.collision, CollisionBallBall)

        ball1 = breakout.balls[0]
        ball2 = breakout.balls[1]
        assert almost_equal_vec(ball1.velocity * ball1.speed, Vec2(x=0, y=0))
        assert almost_equal_vec(ball2.velocity, Vec2(x=1, y=0))


    def test_ball_ball_noncentral_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_ball_angle_stop_collision_level,
    ):
        level, action, ticks = ball_ball_angle_stop_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action.value,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, CollisionEvent)
        assert isinstance(event.collision, CollisionBallBall)

        ball1 = event.collision.ball1
        ball2 = event.collision.ball2
        assert almost_equal_vec(ball1.velocity, Vec2(x=1, y=0))
        assert almost_equal_vec(ball2.velocity, Vec2(x=0, y=-1))
        assert almost_equal_float(ball1.speed, ball2.speed)


    def test_ball_ball_central_towards_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_ball_towards_collision_level,
    ):
        level, action, ticks = ball_ball_towards_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action.value,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, CollisionEvent)
        assert isinstance(event.collision, CollisionBallBall)

        ball1 = breakout.balls[0]
        ball2 = breakout.balls[1]
        assert almost_equal_vec(ball1.velocity, Vec2(x=-1, y=0))
        assert almost_equal_vec(ball2.velocity, Vec2(x=1, y=0))


    def test_ball_ball_central_towards_between_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_ball_towards_between_collision_level,
    ):
        level, action, ticks = ball_ball_towards_between_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action.value,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 3
        for event in events:
            assert isinstance(event, CollisionEvent)
            assert isinstance(event.collision, CollisionBallBall)

        ball1 = breakout.balls[0]
        ball2 = breakout.balls[1]
        ball3 = breakout.balls[2]
        assert almost_equal_vec(ball1.velocity, Vec2(x=-1, y=0))
        assert almost_equal_vec(ball2.velocity, Vec2(x=1, y=0))
        assert almost_equal_vec(ball3.velocity, Vec2(x=0, y=-1))


    def test_ball_ball_central_ghost_race_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_ball_race_collision_level,
    ):
        level, action, ticks = ball_ball_race_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action.value,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        for event in events:
            assert isinstance(event, CollisionEvent)
            assert isinstance(event.collision, CollisionBallBall)

        ball1 = breakout.balls[0]
        ball2 = breakout.balls[1]
        assert almost_equal_vec(ball1.velocity, Vec2(x=1, y=0))
        assert almost_equal_vec(ball2.velocity, Vec2(x=1, y=0))
        assert ball1.speed < ball2.speed
