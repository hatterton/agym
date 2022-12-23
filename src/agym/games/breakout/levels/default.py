import math
from typing import List, Optional

from agym.games.breakout.dtos import Ball, Block, Platform, Wall
from agym.games.breakout.geom import Rectangle, Vec2
from agym.games.breakout.protocols import ILevelBuilder
from agym.games.breakout.state import GameState

from .item_manager import ItemManager


class DefaultLevelBuilder(ILevelBuilder):
    def __init__(
        self,
        env_width: int,
        env_height: int,
        ball_speed: float,
        ball_radius: float,
        platform_speed: float,
        platform_size: Vec2,
        block_wall_num_rows,
        block_size: Vec2,
        block_wall_top_shift: float,
        block_wall_between_shift: float,
    ) -> None:
        self.item_manager = ItemManager()

        self.env_width = env_width
        self.env_height = env_height

        self._ball_speed = ball_speed
        self._ball_radius = ball_radius

        self._platform_speed = platform_speed
        self._platform_size = platform_size

        self._block_wall_num_rows = block_wall_num_rows
        self._block_size = block_size
        self._block_wall_top_shift = block_wall_top_shift
        self._block_wall_between_shift = block_wall_between_shift

    def build(self) -> GameState:
        walls = self._make_walls()

        ball = self.item_manager.create_ball(
            radius=self._ball_radius,
            speed=self._ball_speed,
        )

        platform = self.item_manager.create_platform(
            speed=self._platform_speed,
            width=self._platform_size.x,
            height=self._platform_size.y,
        )
        self._center_platform(platform)

        blocks = self._make_target_wall()

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

        return [
            self.item_manager.create_wall(left_wall),
            self.item_manager.create_wall(top_wall),
            self.item_manager.create_wall(right_wall),
        ]

    def _make_target_wall(
        self,
    ) -> List[Block]:
        between_shift = self._block_wall_between_shift
        top_shift = self._block_wall_top_shift

        block_width = self._block_size.x
        block_height = self._block_size.y

        n_rows = self._block_wall_num_rows
        n_cols = math.floor(
            (self.env_width + between_shift) / (block_width + between_shift)
        )
        side_shift = (
            self.env_width - n_cols * block_width - (n_cols - 1) * between_shift
        ) // 2

        blocks = []
        for i in range(n_rows):
            for j in range(n_cols):
                top = top_shift + i * block_height * 1.5

                centerx = side_shift + (self.env_width - 2 * side_shift) * (
                    j + 1
                ) / (n_cols + 1)
                left = centerx - block_width / 2
                block = self.item_manager.create_block(
                    top=top,
                    left=left,
                    width=block_width,
                    height=block_height,
                    health=1 + (n_rows - i - 1) * 1 + j,
                )
                blocks.append(block)

        return blocks

    def _center_platform(self, platform: Platform) -> None:
        platform.rect.centerx = self.env_width // 2
        platform.rect.bottom = self.env_height - 10
