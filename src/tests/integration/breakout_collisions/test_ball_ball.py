import pytest

from envs.breakout import (
    BreakoutAction,
    BreakoutCollisionEvent,
    BreakoutEnv,
)
from envs.breakout import CollisionBallBall
from geometry import Vec2
from tests.math_utils import almost_equal_float, almost_equal_vec


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
            action=action,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, BreakoutCollisionEvent)
        assert isinstance(event.collision, CollisionBallBall)

        ball1 = breakout._balls[0]
        ball2 = breakout._balls[1]
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
            action=action,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, BreakoutCollisionEvent)
        assert isinstance(event.collision, CollisionBallBall)

        ball1 = breakout._balls[0]
        ball2 = breakout._balls[1]
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
            action=action,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, BreakoutCollisionEvent)
        assert isinstance(event.collision, CollisionBallBall)

        ball1 = breakout._balls[0]
        ball2 = breakout._balls[1]
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
            action=action,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 3
        for event in events:
            assert isinstance(event, BreakoutCollisionEvent)
            assert isinstance(event.collision, CollisionBallBall)

        ball1 = breakout._balls[0]
        ball2 = breakout._balls[1]
        ball3 = breakout._balls[2]
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
            action=action,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        for event in events:
            assert isinstance(event, BreakoutCollisionEvent)
            assert isinstance(event.collision, CollisionBallBall)

        ball1 = breakout._balls[0]
        ball2 = breakout._balls[1]
        assert almost_equal_vec(ball1.velocity, Vec2(x=1, y=0))
        assert almost_equal_vec(ball2.velocity, Vec2(x=1, y=0))
        assert ball1.speed < ball2.speed
