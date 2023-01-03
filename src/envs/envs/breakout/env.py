import random
from typing import Iterable, List

from envs.breakout.dtos import (
    Ball,
    Block,
    BreakoutAction,
    BreakoutActionType,
    BreakoutCollisionEvent,
    BreakoutEvent,
    Collision,
    CollisionBallBall,
    CollisionBallBlock,
    CollisionBallPlatform,
    CollisionBallWall,
    CollisionPlatformWall,
    Platform,
    Wall,
)
from envs.breakout.protocols import IBreakoutLevelBuilder, ICollisionDetector
from envs.protocols import IGameAction, IGameEnvironment
from geometry import Point, Rectangle, Vec2
from timeprofiler import profile

from .state import BreakoutState


class BreakoutEnv(IGameEnvironment):
    def __init__(
        self,
        env_size: Vec2,
        collision_detector: ICollisionDetector,
        level_builder: IBreakoutLevelBuilder,
        checking_gameover: bool = False,
        eps: float = 1e-3,
    ):
        self._env_rect = Rectangle(
            left=0,
            top=0,
            width=env_size.x,
            height=env_size.y,
        )

        self._checking_gameover = checking_gameover
        self._eps = eps

        self._current_timestamp: float
        self._events: List[BreakoutEvent]

        self._level_builder = level_builder
        self._collision_detector = collision_detector

        self._state: BreakoutState

    @property
    def state(self) -> BreakoutState:
        return self._state

    @property
    def _balls(self) -> List[Ball]:
        return self.state.balls

    @property
    def _blocks(self) -> List[Block]:
        return self.state.blocks

    @property
    def _platforms(self) -> List[Platform]:
        return self.state.platforms

    @property
    def _walls(self) -> List[Wall]:
        return self.state.walls

    @property
    def rect(self) -> Rectangle:
        return self._env_rect

    def pop_events(self) -> List[BreakoutEvent]:
        events = self._events
        self._events = []
        return events

    def reset(self) -> None:
        self._reset_level()

        self._current_timestamp = 0.0
        self._events = []

    def _reset_level(self) -> None:
        state = self._level_builder.build()
        self.import_state(state)

    def import_state(self, state: BreakoutState) -> None:
        self._state = state

    def _is_gameover(self) -> bool:
        return False

    def _lose(self) -> None:
        self._reset_level()

    def _win(self) -> None:
        self._reset_level()

    @profile("env_step", "game_update")
    def step(self, action: IGameAction, dt: float) -> bool:
        if not isinstance(action, BreakoutAction):
            raise ValueError("Unknown type of action")

        for platform in self._platforms:
            if action.type == BreakoutActionType.LEFT:
                platform.velocity.x = -1
            elif action.type == BreakoutActionType.RIGHT:
                platform.velocity.x = 1
            elif action.type == BreakoutActionType.THROW:
                self._throw_ball()
            elif action.type == BreakoutActionType.NOTHING:
                platform.velocity.x = 0

        while dt > self._eps:
            step_dt = self._collision_detector.get_time_before_collision(
                self.state, dt
            )
            self._update(step_dt)

            colls = self._collision_detector.get_step_collisions(
                self.state, self._eps
            )

            self._perform_colls(colls)

            dt -= step_dt

        # Проверки на конец игры
        if self._checking_gameover:
            if len(self._blocks) == 0:
                self._win()

            if not self._balls:
                self._lose()

        is_done = self._is_gameover()

        return is_done

    def _perform_colls(self, colls: Iterable[Collision]) -> None:
        for coll in colls:
            self._perform_coll(coll)

    def _perform_coll(self, coll: Collision) -> None:
        self._events.append(
            BreakoutCollisionEvent(
                timestamp=self._current_timestamp,
                collision=coll,
            )
        )

        if isinstance(coll, CollisionBallWall):
            self._perform_ball_coll(ball=coll.ball, point=coll.point)

        elif isinstance(coll, CollisionBallPlatform):
            self._perform_platform_ball_coll(
                platform=coll.platform,
                ball=coll.ball,
                point=coll.point,
            )

        elif isinstance(coll, CollisionBallBlock):
            self._perform_ball_coll(ball=coll.ball, point=coll.point)

            coll.block.health -= 1
            if coll.block.health <= 0:
                self._blocks.remove(coll.block)

        elif isinstance(coll, CollisionPlatformWall):
            coll.platform.velocity.x = 0

        elif isinstance(coll, CollisionBallBall):
            self._perform_ball_ball_coll(
                ball1=coll.ball1,
                ball2=coll.ball2,
                point=coll.point,
            )

    def _perform_ball_coll(self, ball: Ball, point: Point) -> None:
        basis = point - ball.rect.center
        projection = ball.velocity.scalar(basis)
        velocity = ball.velocity - basis * 2.0 * projection / basis.norm2()

        if abs(velocity.y) < 0.1:
            sign = (
                1
                if abs(velocity.y) < self._eps
                else velocity.y / abs(velocity.y)
            )
            velocity.y = sign * 0.1
            velocity /= velocity.norm()

        ball.velocity = velocity

    def _perform_platform_ball_coll(
        self, platform: Platform, ball: Ball, point: Point
    ) -> None:
        p_center = platform.rect.center
        p_center.y += platform.rect.width / 2
        velocity = point - p_center
        velocity = velocity / velocity.norm()

        if ball.rect.centery > platform.rect.centery + 2:
            velocity.y += 0.2
            velocity = velocity / velocity.norm()

        platform.freeze()
        ball.velocity = velocity

    def _perform_ball_ball_coll(
        self, ball1: Ball, ball2: Ball, point: Point
    ) -> None:
        velocity1 = ball1.velocity * ball1.speed
        velocity2 = ball2.velocity * ball2.speed

        velocity_shift = -velocity2

        velocity = velocity1 + velocity_shift
        basis = point - ball1.rect.center
        projection = velocity.scalar(basis)
        leaked_velocity = basis * projection / basis.norm2()

        velocity1 = velocity - leaked_velocity - velocity_shift
        velocity2 = leaked_velocity - velocity_shift

        ball1.speed = velocity1.norm()
        if abs(ball1.speed) < self._eps:
            ball1.velocity = Vec2(x=1, y=0)
        else:
            ball1.velocity = velocity1 / velocity1.norm()

        ball2.speed = velocity2.norm()
        if abs(ball2.speed) < self._eps:
            ball2.velocity = Vec2(x=1, y=0)
        else:
            ball2.velocity = velocity2 / velocity2.norm()

    def _update(self, dt: float) -> None:
        self._current_timestamp += dt

        self._update_platforms(dt)
        self._update_balls(dt)

    def _update_platforms(self, dt: float) -> None:
        for platform in self._platforms:
            fdt = max(0, dt - platform.rest_freeze_time)
            platform.rect.center += platform.velocity * platform.speed * fdt
            platform.rest_freeze_time = max(0, platform.rest_freeze_time - dt)

    def _update_balls(self, dt: float) -> None:
        removed_balls = []
        for ball in self._balls:
            if ball.thrown:
                ball.rect.center += ball.velocity * ball.speed * dt
            else:
                for platform in self._platforms:
                    ball.rect.bottom = platform.rect.top
                    ball.rect.centerx = platform.rect.centerx
                    break
                else:
                    removed_balls.append(ball)

            if ball.rect.top > self._env_rect.bottom:
                removed_balls.append(ball)

        for ball in removed_balls:
            self._balls.remove(ball)

    def _throw_ball(self) -> None:
        for ball in self._balls:
            if not ball.thrown:
                ball.thrown = True
                miss = random.random() - 0.5

                velocity = Vec2(x=miss * 1, y=-1)
                velocity /= velocity.norm()
                ball.velocity = velocity

                ball.rect.bottom -= 1
