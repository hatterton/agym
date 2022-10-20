import random
import pygame
import enum
import numpy as np

from pygame.event import Event as PygameEvent

from typing import (
    Any,
    Tuple,
    List,
    Iterable,
)
from agym.interfaces import IEventHandler

from .levels import DefaultLevelBuilder, PerformanceLevelBuilder, Level
from .events import Event, CollisionEvent
from .geom import Point, Vec2, Rectangle
from agym.games import IGameEnviroment
from agym.games.breakout.items import (
    Ball,
    Platform,
    Block,
)
from agym.games.breakout.protocols import ICollisionDetector
from agym.games.breakout.collisions import (
    CollisionDetector,
    LegacyCollisionDetectorEngine,
    Collision,
    CollisionBallBlock,
    CollisionBallPlatform,
    CollisionBallWall,
    CollisionPlatformWall,
    CollisionBallBall,
)
from .state import GameState

from agym.utils import profile


class BreakoutAction(enum.Enum):
    NOTHING = 0
    LEFT = 1
    RIGHT = 2
    THROW = 3


class BreakoutEnv(IGameEnviroment, IEventHandler):
    def __init__(self, env_width: int, env_height: int,
                 ball_speed: float = 20, platform_speed: float = 15,
                 eps: float = 1e-3):
        self.env_width = env_width
        self.env_height = env_height

        self.env_rect = Rectangle(
            left=0,
            top=0,
            width=self.env_width,
            height=self.env_height,
        )

        self.screen = pygame.Surface((env_width, env_height))

        self.eps = eps
        self.n_actions = 4
        self.start_lives = 1
        self.n_lives: int

        self.timestamp: float
        self.events: List[Event]

        # self.level_builder = DefaultLevelBuilder(
        self.level_builder = PerformanceLevelBuilder(
            env_width=env_width,
            env_height=env_height,
            ball_speed=ball_speed,
            platform_speed=platform_speed,
        )
        self.detector: ICollisionDetector = CollisionDetector(
            engine=LegacyCollisionDetectorEngine(),
        )

        self.balls: List[Ball]
        self.platform: Platform
        self.blocks: List[Block]

    def pop_events(self) -> List[Event]:
        events = self.events
        self.events = []
        return events

    def try_consume_event(self, event: PygameEvent) -> bool:
        return False

    def try_delegate_event(self, event: PygameEvent) -> bool:
        return False

    def reset(self) -> None:
        self.n_lives = self.start_lives

        self.reset_level()

        self.timestamp = 0.
        self.events = []

    def reset_level(self) -> None:
        level = self.level_builder.build()
        self.load_level(level)


    def load_level(self, level: Level) -> None:
        self.balls = level.balls
        self.blocks = level.blocks
        self.platform = level.platform

    def is_done(self):
        return self.n_lives <= 0

    def lose(self):
        self.n_lives -= 1
        self.reset_level()

    def win(self):
        self.reset_level()

    @profile("env_step", "game_update")
    def step(self, action: int, dt: float) -> Tuple[int, bool]:

        a = BreakoutAction(action)
        self.platform.velocity[0] = 0
        if a == BreakoutAction.LEFT:
            self.platform.velocity[0] = -1
        elif a == BreakoutAction.RIGHT:
            self.platform.velocity[0] = 1
        elif a == BreakoutAction.THROW:
            self.throw_ball()
        elif a == BreakoutAction.NOTHING:
            pass

        reward = 0

        while dt > self.eps:
            step_dt = self.detector.get_time_before_collision(self.state, dt)
            self.real_update(step_dt)

            colls = self.detector.get_step_collisions(self.state, self.eps)
            self.perform_colls(colls)

            dt -= step_dt

        # Проверки на конец игры
        if len(self.blocks) == 0:
            self.win()
            reward += 100

        # if self.ball.rect.top > self.env_rect.bottom + 10:
        #     self.lose()
        #     reward -= 100

        is_done = self.is_done()

        return reward, is_done

    @property
    def state(self) -> GameState:
        return GameState(
            platforms=[self.platform],
            balls=self.balls,
            blocks=self.blocks,
            wall_rect=self.env_rect,
        )

    def perform_colls(self, colls: Iterable[Collision]) -> int:
        return self._perform_colls(colls)

    @profile("perf_colls", "env_step")
    def _perform_colls(self, colls: Iterable[Collision]) -> int:
        reward = 0

        for coll in colls:
            self.events.append(
                CollisionEvent(
                    timestamp=self.timestamp,
                    collision=coll,
                )
            )

            if isinstance(coll, CollisionBallWall):
                self.perform_ball_coll(ball=coll.ball, point=coll.point)

            elif isinstance(coll, CollisionBallPlatform):
                self.perform_platform_ball_coll(
                    platform=coll.platform,
                    ball=coll.ball,
                    point=coll.point,
                )

            elif isinstance(coll, CollisionBallBlock):
                self.perform_ball_coll(ball=coll.ball, point=coll.point)

                coll.block.health -= 1
                if coll.block.health <= 0:
                    self.blocks.remove(coll.block)

            elif isinstance(coll, CollisionPlatformWall):
                self.platform.velocity.x = 0

            elif isinstance(coll, CollisionBallBall):
                self.perform_ball_ball_coll(
                    ball1=coll.ball1,
                    ball2=coll.ball2,
                    point=coll.point,
                )


        return reward

    def perform_ball_coll(self, ball: Ball, point: Point) -> None:
        basis = point - ball.rect.center
        projection = ball.velocity.scalar(basis)
        velocity = ball.velocity - basis * 2. * projection / basis.norm2()

        if abs(velocity.y) < 0.1:
            sign = np.sign(velocity.y)
            velocity.y = (sign if sign != 0 else 1) * 0.1
            velocity /= velocity.norm()

        ball.velocity = velocity

    def perform_platform_ball_coll(self, platform: Platform, ball: Ball, point: Point) -> None:
        velocity = point - platform.rect.center
        velocity.x /= 2
        velocity = velocity / velocity.norm()

        if (ball.rect.centery >
            self.platform.rect.centery + 2):
            velocity.y += 0.2
            velocity = velocity / velocity.norm()

        platform.freeze()
        ball.velocity = velocity

    def perform_ball_ball_coll(self, ball1: Ball, ball2: Ball, point: Point) -> None:
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
        if abs(ball1.speed) < self.eps:
            ball1.velocity = Vec2(x=1, y=0)
        else:
            ball1.velocity = velocity1 / velocity1.norm()

        ball2.speed = velocity2.norm()
        if abs(ball2.speed) < self.eps:
            ball2.velocity = Vec2(x=1, y=0)
        else:
            ball2.velocity = velocity2 / velocity2.norm()

    def real_update(self, dt: float) -> None:
        self.timestamp += dt

        self.update_platform(dt)
        self.update_balls(dt)

    def update_platform(self, dt: float) -> None:
        platform: Platform = self.platform
        if platform.rest_freeze_time <= dt:
            dt -= platform.rest_freeze_time
            platform.rect.center += platform.velocity * platform.speed * dt

        if platform.rect.left < 0:
            platform.rect.left = 0

        if platform.rect.right > self.env_width:
            platform.rect.right = self.env_width

        platform.rest_freeze_time = max(0, platform.rest_freeze_time - dt)

    def update_balls(self, dt: float) -> None:
        for ball in self.balls:
            if ball.thrown:
                ball.rect.center += ball.velocity * ball.speed * dt
            else:
                ball.rect.bottom = self.platform.rect.top
                ball.rect.centerx = self.platform.rect.centerx

    def move_ball_on_platform(self, ball: Ball) -> None:
        ball.thrown = False

    def throw_ball(self) -> None:
        for ball in self.balls:
            if not ball.thrown:
                ball.thrown = True
                miss = random.random() - 0.5

                velocity = Vec2(x=miss*1, y=-1)
                velocity /= velocity.norm()
                ball.velocity = velocity

                ball.rect.bottom -= 1

    def blit(self, screen) -> None:
        screen_rect = screen.get_rect()
        self_screen_rect = self.screen.get_rect()
        self_screen_rect.bottom = screen_rect.bottom
        self_screen_rect.centerx = screen_rect.centerx

        self.screen.fill((30, 20, 10))
        self.platform.blit(self.screen)

        for ball in self.balls:
            ball.blit(self.screen)

        for block in self.blocks:
            block.blit(self.screen)

        screen.blit(self.screen, self_screen_rect)

    def try_event(self, event) -> bool:
        if event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.KEYUP:
            pass
        else:
            return False

        return True
