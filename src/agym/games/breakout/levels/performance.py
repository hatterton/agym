import math
import random
from typing import List, Optional

from .item_manager import ItemManager

from agym.games.breakout.items import (
    Ball,
    Block,
    Platform,
    Wall,
)
from agym.games.breakout.geom import (
    Vec2,
    Rectangle,
)
from agym.games.breakout.state import GameState


class PerformanceLevelBuilder:
    def __init__(self, env_width: int, env_height: int, ball_speed: float = 20, platform_speed: float = 15) -> None:
        self.item_manager = ItemManager()

        self.env_width = env_width
        self.env_height = env_height
        self.ball_speed = ball_speed
        self.platform_speed = platform_speed

    def build(self) -> GameState:
        walls = self._make_walls()

        balls = self._make_balls(
            n_balls=2,
            # n_balls=10,
            radius=10,
            # ball_speed=self.ball_speed,
            ball_speed=2,
            shift=100,
        )

        platform = self.item_manager.create_platform(
            speed=self.platform_speed,
        )
        self._center_platform(platform)

        blocks = self._make_target_wall(
            n_rows=6,
        )

        return self.item_manager.extract_state()

    def _make_walls(self) -> List[Wall]:
        return [
            self.item_manager.create_wall(
                rect=Rectangle(
                    left=-1.,
                    top=0.,
                    width=1.,
                    height=self.env_height,
                ),
            ),
            self.item_manager.create_wall(
                rect=Rectangle(
                    left=0.,
                    top=-1.,
                    width=self.env_width,
                    height=1.,
                ),
            ),
            self.item_manager.create_wall(
                rect=Rectangle(
                    left=self.env_width,
                    top=0.,
                    width=1.,
                    height=self.env_height,
                ),
            ),
        ]

    def _make_balls(
        self,
        n_balls: int,
        radius: int,
        ball_speed: int,
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
                speed=ball_speed,
                thrown=True,
            )
            ball.rect.centery = self.env_height / 2
            ball.rect.left = (side_shift + radius * 2) * i + shift
            # print(ball.rect.centerx)
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

