
import math
from typing import Optional, List

from agym.games.breakout.items import (
    Ball,
    Block,
    Platform,
    Wall,
)
from agym.games.breakout.geom import Rectangle
from agym.games.breakout.state import GameState

from .item_manager import ItemManager


class DefaultLevelBuilder:
    def __init__(self, env_width: int, env_height: int, ball_speed: float = 20, platform_speed: float = 15) -> None:
        self.item_manager = ItemManager()

        self.env_width = env_width
        self.env_height = env_height
        self.ball_speed = ball_speed
        self.platform_speed = platform_speed

    def build(self) -> GameState:
        walls = self._make_walls()

        ball = self.item_manager.create_ball(
            radius=10,
            speed=self.ball_speed,
        )

        platform = self.item_manager.create_platform(
            speed=self.platform_speed,
        )
        self._center_platform(platform)

        blocks = self._make_target_wall()

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

    def _make_target_wall(self,
                          n_rows: int = 4,
                          block_width: int = 60,
                          block_height: int = 20,
                          top_shift: int = 50,
                          between_shift: int = 5) -> List[Block]:
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

        blocks = []
        for i in range(n_rows):
            for j in range(n_cols):
                top = (top_shift + i * block_height +
                       (i - 1) * between_shift)
                left = (side_shift + j * block_width +
                        (j - 1) * between_shift)
                block = self.item_manager.create_block(
                    top=top,
                    left=left
                )
                blocks.append(block)

        return blocks

    def _center_platform(self, platform: Platform) -> None:
        platform.rect.centerx = self.env_width // 2
        platform.rect.bottom = self.env_height - 10

