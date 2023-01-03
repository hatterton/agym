import pytest

from envs.breakout import BreakoutCollisionEvent, BreakoutEnv, CollisionBallWall


@pytest.mark.breakout
@pytest.mark.collisions
@pytest.mark.ball
@pytest.mark.wall
class TestCollisionsBallWall:
    def test_ball_vertical_wall_left_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_vertical_wall_left_collision_level,
    ):
        level, action, ticks = ball_vertical_wall_left_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, BreakoutCollisionEvent)
        assert isinstance(event.collision, CollisionBallWall)
        assert breakout._balls[0].velocity[0] > 0
        assert breakout._balls[0].velocity[1] < 0

    def test_ball_vertical_wall_right_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_vertical_wall_right_collision_level,
    ):
        level, action, ticks = ball_vertical_wall_right_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, BreakoutCollisionEvent)
        assert isinstance(event.collision, CollisionBallWall)
        assert breakout._balls[0].velocity[0] < 0
        assert breakout._balls[0].velocity[1] < 0

    def test_ball_horisontal_wall_top_collision_type(
        self,
        breakout: BreakoutEnv,
        ball_horisontal_wall_top_collision_level,
    ):
        level, action, ticks = ball_horisontal_wall_top_collision_level
        breakout.import_state(level)

        breakout.step(
            action=action,
            dt=ticks,
        )

        events = breakout.pop_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, BreakoutCollisionEvent)
        assert isinstance(event.collision, CollisionBallWall)
        assert breakout._balls[0].velocity[0] > 0
        assert breakout._balls[0].velocity[1] > 0
