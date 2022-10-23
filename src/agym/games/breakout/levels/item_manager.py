
import random
from typing import Optional, List

from agym.games.breakout.items import (
    Platform,
    Ball,
    Block,
    Wall,
)
from agym.games.breakout.geom import (
    Rectangle,
)


class ItemManager:
    def __init__(self) -> None:
        self.item_counter = 0

    def _tick(self) -> int:
        res = self.item_counter
        self.item_counter += 1

        return res

    def create_wall(self, rect: Rectangle) -> Wall:
        return Wall(
            rect=rect,
            item_id=self._tick(),
        )

    def create_block(self, top: int, left: int, health: int = 1) -> Block:
        image_name_template = "block_{} 60x20.png"
        colors = ["blue", "yellow", "red"]
        image_name = image_name_template.format(random.choice(colors))

        return Block(
            image_name=image_name,
            top=top,
            left=left,
            health=health,
            item_id=self._tick(),
        )

    def create_platform(self, speed: float) -> Platform:
        image_name = "platform 120x20.png"

        return Platform(
            image_name=image_name,
            speed=speed,
            item_id=self._tick(),
        )

    def create_ball(self, radius: float, speed: float, thrown: bool = False, top: Optional[float] = None, left: Optional[float] = None) -> Ball:
        image_name = "ball_aparture 20x20.png"

        ball = Ball(
            image_name=image_name,
            radius=radius,
            speed=speed,
            thrown=thrown,
            item_id=self._tick(),
        )

        if top is not None:
            ball.rect.top = top

        if left is not None:
            ball.rect.left = left

        return ball

