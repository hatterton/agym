import math
import random
from typing import List, Optional

from agym.games.breakout.dtos import Ball, Block, Platform, Wall
from agym.games.breakout.geom import Rectangle, Vec2
from agym.games.breakout.protocols import ILevelBuilder
from agym.games.breakout.state import GameState

from .item_manager import ItemManager


class PerformanceLevelBuilder(ILevelBuilder):
    def __init__(
        self,
        env_width: int,
        env_height: int,
        num_balls: int = 10,
        ball_radius: float = 10.0,
        ball_speed: float = 20.0,
    ) -> None:
        self._item_manager = ItemManager()

        self._env_width = env_width
        self._env_height = env_height

        self._num_balls = num_balls
        self._ball_radius = ball_radius
        self._ball_speed = ball_speed

    def build(self) -> GameState:
        walls = self._make_walls()

        balls = self._make_balls(
            n_balls=self._num_balls,
            radius=self._ball_radius,
            ball_speed=self._ball_speed,
            shift=100,
        )

        return self._item_manager.extract_state()

    def _make_walls(self) -> List[Wall]:
        shift = 5.0
        left = shift
        top = shift
        right = self._env_width - shift
        bottom = self._env_width - shift

        width = right - left
        height = bottom - top

        wall_width = 3.0

        left_wall = Rectangle(
            left=left,
            top=top,
            width=wall_width,
            height=height,
        )

        top_wall = Rectangle(
            left=left,
            top=top,
            width=width,
            height=wall_width,
        )

        right_wall = Rectangle(
            left=left,
            top=top,
            width=wall_width,
            height=height,
        )
        right_wall.right = right

        bottom_wall = Rectangle(
            left=left,
            top=top,
            width=width,
            height=wall_width,
        )
        bottom_wall.bottom = bottom

        return [
            self._item_manager.create_wall(left_wall),
            self._item_manager.create_wall(top_wall),
            self._item_manager.create_wall(right_wall),
            self._item_manager.create_wall(bottom_wall),
        ]

    def _make_balls(
        self,
        n_balls: int,
        radius: float,
        ball_speed: float,
        shift: int = 100,
    ):
        n = 1
        while n**2 < n_balls:
            n += 1

        velocities = [
            [i / (i**2 + j**2) ** 0.5, j / (i**2 + j**2) ** 0.5]
            for i in range(-10, 10)
            for j in range(-10, 10)
            if i != 0 or j != 0
        ]

        balls = []
        for i in range(n_balls):
            row = i // n
            col = i % n

            ball = self._item_manager.create_ball(
                radius=radius,
                speed=ball_speed,
                thrown=True,
            )

            ball.rect.centerx = (col + 1) * self._env_width / (n + 1)
            ball.rect.centery = (row + 1) * self._env_height / (n + 1)

            velocity = random.choice(velocities).copy()
            ball.velocity = Vec2.from_list(velocity)

            balls.append(ball)

        return balls

    def _make_target_wall(
        self,
        n_rows: int = 6,
        block_width: int = 60,
        block_height: int = 20,
        top_shift: int = 50,
        horisontal_shift: int = 5,
        vertical_shift: int = 19,
        health: int = 100,
    ) -> List[Block]:
        n_cols = (
            math.floor(
                (self._env_width - block_width)
                / (block_width + horisontal_shift)
            )
            + 1
        )
        side_shift = (
            self._env_width
            - n_cols * block_width
            - (n_cols - 1) * horisontal_shift
        ) // 2

        blocks = []
        for i in range(n_rows):
            for j in range(n_cols):
                if i not in [0, n_rows - 1] and j not in [0, n_cols - 1]:
                    continue

                top = top_shift + i * block_height + i * vertical_shift
                left = side_shift + j * block_width + j * horisontal_shift
                block = self._item_manager.create_block(
                    top=top,
                    left=left,
                    health=health,
                )
                blocks.append(block)

        return blocks
