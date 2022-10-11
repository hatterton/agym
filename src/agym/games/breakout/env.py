import math
import random
import pygame
import enum
import numpy as np

from pygame.event import Event as PygameEvent
from .events import Event, CollisionEvent
from .geom import Point
from agym.games import IGameEnviroment
from agym.games.breakout.items import (
    Ball,
    Platform,
    Block,
)
from agym.games.breakout.collision import (
    Collision,
    CollisionType,
    calculate_colls,
    normalize,
)
from typing import (
    Any,
    Tuple,
    List,
)
from agym.interfaces import IEventHandler
from pygame.sprite import Group
from collections import namedtuple
from itertools import product
from .level_builder import DefaultLevelBuilder, Level
from agym.utils import profile


class BreakoutAction(enum.Enum):
    NOTHING = 0
    LEFT = 1
    RIGHT = 2
    THROW = 3


class BreakoutEnv(IGameEnviroment, IEventHandler):
    def __init__(self, env_width: int, env_height: int,
                 map_shape: List[int], eps: float = 1e-3):
        self.env_width = env_width
        self.env_height = env_height

        self.screen = pygame.Surface((env_width, env_height))

        self.eps = eps
        self.n_actions = 4
        self.start_lives = 1
        self.n_lives: int

        self.timestamp: float
        self.events: List[Event]

        # self.map_shape = map_shape
        # self.last_state: np.ndarray

        self.level_builder = DefaultLevelBuilder(
            env_width=env_width,
            env_height=env_height,
        )
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
        # self.last_state = self.get_cur_state()
        Rect = namedtuple("Rect", "top bottom left right")
        env_rect = Rect(top=0, bottom=self.env_height,
                        left=0, right=self.env_width)

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
        candidates = self.get_available_blocks(self.eps)
        colls = calculate_colls(env_rect, self.platform,
                                self.ball, candidates, self.eps)
        # platform near wall
        if (len(colls) == 1 and
            colls[0].type == CollisionType.PLATFORM_WALL):
            self.perform_colls(colls)

        candidates = self.get_available_blocks(dt)
        colls = calculate_colls(env_rect, self.platform,
                                self.ball, candidates, dt)

        if len(colls) == 0:
            self.real_update(dt)
        else:
            while dt > self.eps:
                min_dt, max_dt = 0.0, dt
                while max_dt - min_dt > self.eps:
                    possible_dt = (max_dt + min_dt) / 2

                    candidates = self.get_available_blocks(possible_dt)
                    colls = calculate_colls(env_rect, self.platform,
                                            self.ball, candidates,
                                            possible_dt)
                    if len(colls) == 0:
                        min_dt = possible_dt
                    else:
                        max_dt = possible_dt

                self.real_update(min_dt)
                candidates = self.get_available_blocks(self.eps)
                colls = calculate_colls(env_rect, self.platform,
                                        self.ball, candidates, self.eps)
                reward += self.perform_colls(colls)
                dt -= min_dt

        # Проверки на конец игры
        if len(self.blocks) == 0:
            self.win()
            reward += 100

        if self.ball.rect.top > env_rect.bottom + 10:
            self.lose()
            reward -= 100

        is_done = self.is_done()

        return reward, is_done

    def get_available_blocks(self, dt: float) -> List[Block]:
        available_blocks = []

        for block in self.blocks:
            w, h = block.rect.w, block.rect.h
            diag = (w ** 2 + h ** 2) ** 0.5
            min_dist = (diag + self.ball.radius +
                        self.ball.velocity * dt)

            dist = (
                (block.rect.centerx - self.ball.rect.centerx) ** 2 +
                (block.rect.centery - self.ball.rect.centery) ** 2
            ) ** 0.5

            if dist < min_dist + 10 * self.eps:
                available_blocks.append(block)


        return available_blocks

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

    def perform_colls(self, colls) -> int:
        reward = 0

        for coll in colls:
            self.events.append(
                CollisionEvent(
                    timestamp=self.timestamp,
                    collision_type=coll.type,
                    point=Point(
                        x=coll.point[0],
                        y=coll.point[1],
                    ),
                )
            )

            if coll.type == CollisionType.BALL_WALL:
                self.perform_ball_coll(coll.point)

            elif coll.type == CollisionType.BALL_PLATFORM:
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

            elif coll.type == CollisionType.BALL_BLOCK:
                self.perform_ball_coll(coll.point)
                self.blocks.remove(coll.block)
                reward += 10

            elif coll.type == CollisionType.PLATFORM_WALL:
                reward -= 10
                self.platform.vec_velocity[0] = 0


        return reward

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
            ball.vec_velocity = [miss*4, -1]
            ball.vec_velocity = normalize(ball.vec_velocity)

            self.ball.rect.bottom -= 1

    def intersect(self, rect_a, rect_b):
        left = max(rect_a.left, rect_b.left)
        right = min(rect_a.right, rect_b.right)
        top = max(rect_a.top, rect_b.top)
        bottom = min(rect_a.bottom, rect_b.bottom)

        dx = right - left
        dy = bottom - top

        result: float
        if dx < 0 or dy < 0:
            result = 0
        else:
            result = dx * dy

        return result

    def build_map(self, items):
        item_map = np.zeros(self.map_shape, dtype="float32")
        n_rows, n_cols = self.map_shape

        box_w = self.env_width / n_cols
        box_h = self.env_height / n_rows

        for item in items:
            for i, j in product(range(n_rows), range(n_cols)):
                box = pygame.Rect(j * box_w, i * box_h, box_w, box_h)
                item_map[i, j] += self.intersect(box, item.rect)

        item_map /= box_h * box_w

        return item_map

    # def get_cur_state(self):
    #     ball_map = self.build_map([self.ball])
    #     platform_map = self.build_map([self.platform])
    #     break_map = self.build_map(self.blocks)

    #     state = np.stack([ball_map, platform_map, break_map], axis=0)

    #     return state

    # def get_visual_state(self):
    #     cur_state = self.get_cur_state()
    #     state = np.concatenate([self.last_state, cur_state], axis=0)
    #     return state

    # def get_flatten_state(self):
    #     return None

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
            # if event.key == pygame.K_SPACE:
            #     self.throw_ball()
            pass
        elif event.type == pygame.KEYUP:
            pass
        else:
            return False

        return True
