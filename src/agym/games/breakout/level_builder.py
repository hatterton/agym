import random
import math

from typing import List
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .items import Platform, Ball, Block


@dataclass
class Level:
    platform: Platform
    balls: List[Ball]
    blocks: List[Block]


class ItemManager:
    def __init__(self) -> None:
        self.item_counter = 0

    def create_block(self, top: int, left: int) -> Block:
        image_name_template = "block_{} 60x20.png"
        colors = ["blue", "yellow", "red"]
        image_name = image_name_template.format(random.choice(colors))

        block = Block(
            image_name=image_name,
            top=top,
            left=left,
            item_id=self.item_counter,
        )
        self.item_counter += 1

        return block

    def create_platform(self, velocity: float) -> Platform:
        image_name = "platform 120x20.png"

        platform = Platform(
            image_name=image_name,
            velocity=velocity,
            item_id=self.item_counter,
        )
        self.item_counter += 1

        return platform

    def create_ball(self, radius: float, velocity: float) -> Ball:
        image_name = "ball_aparture 20x20.png"

        ball = Ball(
            image_name=image_name,
            radius=radius,
            velocity=velocity,
            item_id=self.item_counter,
        )
        self.item_counter += 1

        return ball


class ILevelBuilder(ABC):
    @abstractmethod
    def build(self) -> Level:
        pass


class DefaultLevelBuilder(ILevelBuilder):
    def __init__(self, env_width: int, env_height: int) -> None:
        self.item_manager = ItemManager()

        self.env_width = env_width
        self.env_height = env_height

    def build(self) -> Level:
        ball = self.item_manager.create_ball(
            radius=10,
            velocity=20,
        )

        platform = self.item_manager.create_platform(
            velocity=15,
        )
        self._center_platform(platform)

        blocks = self._make_target_wall()

        return Level(
            platform=platform,
            balls=[ball],
            blocks=blocks,
        )

    def _make_target_wall(self,
                          n_rows: int = 5,
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

