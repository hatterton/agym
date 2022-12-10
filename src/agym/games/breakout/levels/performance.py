import math
import random
from typing import List, Optional

from agym.games.breakout.dtos import Ball, Block, Platform, Wall
from agym.games.breakout.geom import Rectangle, Vec2
from agym.games.breakout.state import GameState

from .item_manager import ItemManager


class PerformanceLevelBuilder:
    def __init__(
        self,
        env_width: int,
        env_height: int,
        ball_speed: float = 20,
        platform_speed: float = 15,
    ) -> None:
        self.item_manager = ItemManager()

        self.env_width = env_width
        self.env_height = env_height
        self.ball_speed = ball_speed
        self.platform_speed = platform_speed

    def build(self) -> GameState:
        walls = self._make_walls()

        balls = self._make_balls(
            n_balls=10,
            radius=10,
            ball_speed=self.ball_speed,
            shift=100,
        )

        return self.item_manager.extract_state()

    def _make_walls(self) -> List[Wall]:
        shift = 5.0
        left = shift
        top = shift
        right = self.env_width - shift
        bottom = self.env_width - shift

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
            self.item_manager.create_wall(left_wall),
            self.item_manager.create_wall(top_wall),
            self.item_manager.create_wall(right_wall),
            self.item_manager.create_wall(bottom_wall),
        ]

    def _make_balls(
        self,
        n_balls: int,
        radius: int,
        ball_speed: float,
        shift: int = 100,
    ):
        balls = []
        velocities = [
            [i / (i**2 + j**2) ** 0.5, j / (i**2 + j**2) ** 0.5]
            for i in range(-10, 10)
            for j in range(-10, 10)
            if i != 0 or j != 0
        ]

        side_shift = (self.env_width - shift * 2 - n_balls * radius * 2) // max(
            1, n_balls - 1
        )

        for i in range(n_balls):
            ball = self.item_manager.create_ball(
                radius=radius,
                speed=ball_speed,
                thrown=True,
            )
            ball.rect.centery = self.env_height / 2
            ball.rect.left = (side_shift + radius * 2) * i + shift
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
                (self.env_width - block_width)
                / (block_width + horisontal_shift)
            )
            + 1
        )
        side_shift = (
            self.env_width
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
                block = self.item_manager.create_block(
                    top=top,
                    left=left,
                    health=health,
                )
                blocks.append(block)

        return blocks
