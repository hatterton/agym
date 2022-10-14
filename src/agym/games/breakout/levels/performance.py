import math
import random
from typing import List, Optional

from .item_manager import ItemManager
from .level import Level

from ..items import Ball, Block, Platform


class PerformanceLevelBuilder:
    def __init__(self, env_width: int, env_height: int, ball_velocity: float = 20, platform_velocity: float = 15) -> None:
        self.item_manager = ItemManager()

        self.env_width = env_width
        self.env_height = env_height
        self.ball_velocity = ball_velocity
        self.platform_velocity = platform_velocity

    def build(self) -> Level:
        balls = self._make_balls(
            n_balls=5,
            radius=10,
            ball_velocity=self.ball_velocity,
            # ball_velocity=0,
            shift=100,
        )

        platform = self.item_manager.create_platform(
            velocity=self.platform_velocity,
        )
        self._center_platform(platform)

        blocks = self._make_target_wall(
            n_rows=4,
        )

        return Level(
            platform=platform,
            balls=balls,
            blocks=blocks,
        )

    def _make_balls(
        self,
        n_balls: int,
        radius: int,
        ball_velocity: int,
        shift: int = 100,
    ):
        balls = []
        velocities = [
            [i / (i**2 + j**2)**0.5, j / (i**2 + j**2)**0.5]
            for i in range(-10, 10)
            for j in range(-10, 10)
            if i != 0 or j != 0
        ]

        side_shift = (
            self.env_width -
            shift * 2 -
            n_balls * radius * 2
        ) // max(1, n_balls - 1)

        for i in range(n_balls):
            ball = self.item_manager.create_ball(
                radius=radius,
                velocity=ball_velocity,
                thrown=True,
            )
            ball.rect.centery = self.env_height / 2
            ball.rect.left = (side_shift + radius * 2) * i + shift
            # print(ball.rect.centerx)
            ball.vec_velocity = random.choice(velocities).copy()

            balls.append(ball)

        return balls

    def _make_target_wall(
        self,
        n_rows: int = 5,
        block_width: int = 60,
        block_height: int = 20,
        top_shift: int = 50,
        horisontal_shift: int = 10,
        vertical_shift: int = 40,
        health: int = 100,
    ) -> List[Block]:
        image_name_template = "block_{} 60x20.png"
        colors = ["blue", "yellow", "red"]

        n_cols = math.floor(
            (self.env_width - block_width) /
            (block_width + horisontal_shift)
        ) + 1
        side_shift = (
            self.env_width -
            n_cols * block_width -
            (n_cols - 1) * horisontal_shift
        ) // 2

        blocks = []
        for i in range(n_rows):
            for j in range(n_cols):
                if i not in [0, n_rows -1] and j not in [0, n_cols -1]:
                    continue

                top = (top_shift + i * block_height +
                       i * vertical_shift)
                left = (side_shift + j * block_width +
                        j * horisontal_shift)
                block = self.item_manager.create_block(
                    top=top,
                    left=left,
                    health=health,
                )
                blocks.append(block)

        return blocks

    def _center_platform(self, platform: Platform) -> None:
        platform.rect.centerx = self.env_width // 2
        platform.rect.bottom = self.env_height - 10

