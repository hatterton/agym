import math
import random
import pygame
import enum
import numpy as np

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
)
from pygame.sprite import Group
from collections import namedtuple
from pprint import pprint

class BreakoutAction(enum.Enum):
    NOTHING = 0
    LEFT = 1
    RIGHT = 2
    THROW = 3


class BreakoutEnv(IGameEnviroment):
    def __init__(self, env_width: int, env_height: int,
                 eps: float = 1e-3):
        self.env_width = env_width
        self.env_height = env_height
        self.eps = eps
        self.n_actions = 4
        self.start_lives = 1
        self.n_lives: int

        self.ball = Ball(
            image_name="ball_aparture 20x20.png",
            radius=10,
            velocity=20,
        )
        self.platform = Platform(
            image_name="platform 120x20.png",
            velocity=15,
        )
        self.blocks = Group()

    def center_platform(self):
        self.platform.rect.centerx = self.env_width // 2
        self.platform.rect.bottom = self.env_height - 10

    def reset(self):
        self.n_lives = self.start_lives
        self.make_target_wall()
        self.center_platform()
        self.move_ball_on_platform()

    def is_done(self):
        return self.n_lives <= 0

    def lose(self):
        self.n_lives -= 1
        self.center_platform()
        self.move_ball_on_platform()

    def win(self):
        self.make_target_wall()
        self.center_platform()
        self.move_ball_on_platform()

    def make_target_wall(self,
                         n_rows: int = 5,
                         block_width: int = 60,
                         block_height: int = 20,
                         top_shift: int = 50,
                         between_shift: int = 5):
        image_name_template = "block_{} 60x20.png"
        colors = ["blue", "yellow", "red"]

        n_cols = math.floor(
            (self.env_width - between_shift) /
            (block_width + between_shift)
        )
        side_shift = (
            self.env_width -
            n_cols * block_width -
            (n_cols - 1) * between_shift
        ) // 2

        self.blocks.empty()
        for i in range(n_rows):
            for j in range(n_cols):
                image_name = image_name_template.format(
                    colors[random.randint(0, 2)]
                )
                top = (top_shift + i * block_height +
                       (i - 1) * between_shift)
                left = (side_shift + j * block_width +
                        (j - 1) * between_shift)
                block = Block(
                    image_name=image_name,
                    top=top,
                    left=left
                )
                self.blocks.add(block)

    def step(self, action: int, dt: float) -> Tuple[int, bool]:
        Rect = namedtuple("Rect", "top bottom left right")
        env_rect = Rect(top=0, bottom=self.env_height,
                        left=0, right=self.env_width)

        # print(action)
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
        # condidates = get_collision_candidates(dt)
        colls = calculate_colls(env_rect, self.platform,
                                self.ball, self.blocks, dt)
        if len(colls) == 0:
            self.real_update(dt)
        else:
            while dt > self.eps:
                min_dt, max_dt = 0.0, dt
                while max_dt - min_dt > self.eps:
                    possible_dt = (max_dt + min_dt) / 2

                    colls = calculate_colls(env_rect, self.platform,
                                            self.ball, self.blocks,
                                            possible_dt)
                    if len(colls) == 0:
                        min_dt = possible_dt
                    else:
                        max_dt = possible_dt

                self.real_update(min_dt)
                colls = calculate_colls(env_rect, self.platform,
                                        self.ball, self.blocks, self.eps)
                reward += self.perform_colls(colls)
                dt -= min_dt
                # break

        # Проверки на конец игры
        if len(self.blocks) == 0:
            self.win()

        if self.ball.rect.top > env_rect.bottom + 10:
            self.lose()

        is_done = self.is_done()

        return reward, is_done

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

        self.ball.vec_velocity = new_vel


    def perform_colls(self, colls) -> int:
        reward = 0

        if len(colls) != 0:
            print("Length of coll = {}".format(len(colls)))

        for coll in colls:
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

            elif coll.type == CollisionType.BALL_BLOCK:
                self.perform_ball_coll(coll.point)
                self.blocks.remove(coll.block)
                reward += 10

            elif coll.type == CollisionType.PLATFORM_WALL:
                self.platform.vec_velocity[0] = 0


        return reward

    def real_update(self, dt: float) -> None:
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
            ball.rect.bottom = self.platform.rect.top
            ball.rect.centerx = self.platform.rect.centerx

    def move_ball_on_platform(self) -> None:
        ball = self.ball
        ball.thrown = False
        ball.rect.bottom = self.platform.rect.top
        ball.rect.centerx = self.platform.rect.centerx

    def throw_ball(self) -> None:
        ball = self.ball
        if not self.ball.thrown:
            ball.thrown = True
            miss = random.random() - 0.5
            ball.vec_velocity = [miss*4, -1]
            ball.vec_velocity = normalize(ball.vec_velocity)

            self.ball.rect.bottom = self.platform.rect.top - 1

    def get_visual_state(self, n_binarizing_box: int = 10):
        shape = [4, n_binarizing_box, n_binarizing_box]
        state = np.random.random(size=np.prod(shape))
        state = state.astype("float32").reshape(shape)
        # print(state.dtype)
        # sel1 = agym.param.left_side < self.rect.right
        # sel2 = agym.param.right_side > self.rect.left
        # sel3 = np.logical_and(sel1, sel2)
        # sel4 = agym.param.top_side < self.rect.bottom
        # sel5 = agym.param.bottom_side > self.rect.top
        # sel6 = np.logical_and(sel4, sel5)

        # sel7 = np.logical_and(sel3[np.newaxis, :], sel6[:, np.newaxis])
        # self.intersected = np.transpose(sel7)
        return state

    def get_flatten_state(self):
        return None

    def blit(self, screen) -> None:
        self.platform.blit(screen)
        self.ball.blit(screen)
        for block in self.blocks:
            block.blit(screen)
        # self.blocks.draw(screen)

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
