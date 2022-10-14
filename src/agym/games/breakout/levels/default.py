
import math
from typing import Optional, List

from ..items import Platform, Ball, Block

from .level import Level
from .item_manager import ItemManager


class DefaultLevelBuilder:
    def __init__(self, env_width: int, env_height: int, ball_velocity: float = 20, platform_velocity: float = 15) -> None:
        self.item_manager = ItemManager()

        self.env_width = env_width
        self.env_height = env_height
        self.ball_velocity = ball_velocity
        self.platform_velocity = platform_velocity

    def build(self) -> Level:
        ball = self.item_manager.create_ball(
            radius=10,
            velocity=self.ball_velocity,
        )

        platform = self.item_manager.create_platform(
            velocity=self.platform_velocity,
        )
        self._center_platform(platform)

        blocks = self._make_target_wall()

        return Level(
            platform=platform,
            balls=[ball],
            blocks=blocks,
        )

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

