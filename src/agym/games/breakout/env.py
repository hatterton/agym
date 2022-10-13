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
from collections import namedtuple

from .level_builder import DefaultLevelBuilder, Level
from .events import Event, CollisionEvent
from .geom import Point
from agym.games import IGameEnviroment
from agym.games.breakout.items import (
    Ball,
    Platform,
    Block,
)
from .protocols import ICollisionDetector
from .collisions.legacy_collision import normalize
from .collisions import (
    LegacyCollisionDetector,
    Collision,
    CollisionBallBlock,
    CollisionBallPlatform,
    CollisionBallWall,
    CollisionPlatformWall,
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
                 ball_velocity: float = 20, platform_velocity: float = 15,
                 eps: float = 1e-3):
        self.env_width = env_width
        self.env_height = env_height

        Rect = namedtuple("Rect", "top bottom left right")
        self.env_rect = Rect(top=0, bottom=self.env_height,
                             left=0, right=self.env_width)

        self.screen = pygame.Surface((env_width, env_height))

        self.eps = eps
        self.n_actions = 4
        self.start_lives = 1
        self.n_lives: int

        self.timestamp: float
        self.events: List[Event]

        self.level_builder = DefaultLevelBuilder(
            env_width=env_width,
            env_height=env_height,
            ball_velocity=ball_velocity,
            platform_velocity=platform_velocity,
        )
        self.collision_detector: ICollisionDetector = LegacyCollisionDetector()
        self.ball: Ball
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
        # self.last_state = self.get_cur_state()
        self.n_lives = self.start_lives

        self.reset_level()

        self.timestamp = 0.
        self.events = []

    def reset_level(self) -> None:
        level = self.level_builder.build()
        self.load_level(level)


    def load_level(self, level: Level) -> None:
        self.ball = level.balls[0]
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
        self.platform.vec_velocity[0] = 0
        if a == BreakoutAction.LEFT:
            self.platform.vec_velocity[0] = -1
        elif a == BreakoutAction.RIGHT:
            self.platform.vec_velocity[0] = 1
        elif a == BreakoutAction.THROW:
            self.throw_ball()
        elif a == BreakoutAction.NOTHING:
            pass

        reward = 0

        # платформа возле стены
        colls = self._get_step_collisions(self.eps)
        self.perform_colls(colls)

        # многоступенчатое определение времени столкновения
        colls = self._get_step_collisions(dt)
        if not self._any_colls(colls):
            self.real_update(dt)
        else:
            while dt > self.eps:
                min_dt, max_dt = 0.0, dt
                while max_dt - min_dt > self.eps:
                    possible_dt = (max_dt + min_dt) / 2

                    colls = self._get_step_collisions(possible_dt)

                    if not self._any_colls(colls):
                        min_dt = possible_dt
                    else:
                        max_dt = possible_dt

                self.real_update(min_dt)
                colls = self._get_step_collisions(self.eps)
                reward += self.perform_colls(colls)
                dt -= min_dt

        # Проверки на конец игры
        if len(self.blocks) == 0:
            self.win()
            reward += 100

        if self.ball.rect.top > self.env_rect.bottom + 10:
            self.lose()
            reward -= 100

        is_done = self.is_done()

        return reward, is_done

    def _get_step_collisions(self, dt: float) -> Iterable[Collision]:
        return self.collision_detector.generate_step_collisions(
            state=self._get_state(),
            dt=dt,
        )

    def _get_state(self) -> GameState:
        return GameState(
            platforms=[self.platform],
            balls=[self.ball],
            blocks=self.blocks,
            wall_rect=self.env_rect,
        )

    @profile("any_colls", "env_step")
    def _any_colls(self, colls: Iterable[Collision]) -> bool:
        return any(colls)

    def perform_colls(self, colls: Iterable[Collision]) -> int:
        return self._perform_colls(self._get_all_colls(colls))

    @profile("all_colls", "env_step")
    def _get_all_colls(self, colls: Iterable[Collision]) -> List[Collision]:
        return list(colls)

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
                self.perform_ball_coll(coll.point)

            elif isinstance(coll, CollisionBallPlatform):
                new_vel = [coll.point[i] - self.platform.rect.center[i]
                           for i in range(2)]
                new_vel[0] /= 2
                new_vel = normalize(new_vel)

                if (self.ball.rect.centery >
                    self.platform.rect.centery + 2):
                    new_vel[1] += 0.2
                    new_vel = normalize(new_vel)

                self.platform.freeze()
                self.ball.vec_velocity = new_vel
                reward += 10

            elif isinstance(coll, CollisionBallBlock):
                self.perform_ball_coll(coll.point)
                self.blocks.remove(coll.block)
                reward += 10

            elif isinstance(coll, CollisionPlatformWall):
                reward -= 10
                self.platform.vec_velocity[0] = 0


        return reward

    def perform_ball_coll(self, point) -> None:
        if point is None:
            raise ValueError("What the fuck!!!")

        vel = self.ball.vec_velocity
        basis = [point[i] - self.ball.rect.center[i]
                 for i in range(2)]

        basis = normalize(basis)

        projection = sum([vel[i] * basis[i] for i in range(2)])
        new_vel = [vel[i] - 2.0 * projection * basis[i]
                   for i in range(2)]
        new_vel = normalize(new_vel)
        if abs(new_vel[1]) < 0.1:
            sign = np.sign(new_vel[1])
            new_vel[1] =  (sign if sign != 0 else 1) * 0.1
            new_vel = normalize(new_vel)

        self.ball.vec_velocity = new_vel

    def real_update(self, dt: float) -> None:
        self.timestamp += dt

        self.update_platform(dt)
        self.update_ball(dt)

    def update_platform(self, dt: float) -> None:
        platform: Platform = self.platform
        if platform.rest_freeze_time <= dt:
            dt -= platform.rest_freeze_time
            platform.rect.centerx += (platform.velocity * dt *
                                      platform.vec_velocity[0])

        platform.rest_freeze_time = max(0, platform.rest_freeze_time - dt)

    def update_ball(self, dt: float) -> None:
        ball = self.ball
        if ball.thrown:
            for i in range(2):
                ball.rect.center[i] += (
                    ball.velocity * ball.vec_velocity[i] * dt)
        else:
            # ball.rect.bottom = self.platform.rect.top
            ball.rect.centery = self.platform.rect.top - ball.radius
            ball.rect.centerx = self.platform.rect.centerx

    def move_ball_on_platform(self) -> None:
        ball = self.ball
        ball.thrown = False
        # ball.rect.centery = self.platform.rect.top - ball.radius - 1
        # ball.rect.centerx = self.platform.rect.centerx

    def throw_ball(self) -> None:
        ball = self.ball
        if not self.ball.thrown:
            ball.thrown = True
            miss = random.random() - 0.5
            ball.vec_velocity = [miss*1, -1]
            ball.vec_velocity = normalize(ball.vec_velocity)

            self.ball.rect.bottom -= 1

    def blit(self, screen) -> None:
        screen_rect = screen.get_rect()
        self_screen_rect = self.screen.get_rect()
        self_screen_rect.bottom = screen_rect.bottom
        self_screen_rect.centerx = screen_rect.centerx

        self.screen.fill((30, 20, 10))
        self.platform.blit(self.screen)
        self.ball.blit(self.screen)

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
