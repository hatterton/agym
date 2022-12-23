import random
from typing import List, Optional

from agym.games.breakout.dtos import Ball, Block, Platform, Wall
from agym.games.breakout.geom import Rectangle
from agym.games.breakout.state import GameState


class ItemManager:
    def __init__(self) -> None:
        self.item_counter = 0

        self._state: GameState
        self.reset()

    def _tick(self) -> int:
        res = self.item_counter
        self.item_counter += 1

        return res

    def reset(self) -> None:
        self._state = GameState()

    def extract_state(self) -> GameState:
        res = self._state
        self.reset()

        return res

    def create_wall(self, rect: Rectangle) -> Wall:
        wall = Wall(
            id=self._tick(),
            rect=rect,
        )
        self._state.walls.append(wall)

        return wall

    def create_block(
        self,
        top: float,
        left: float,
        width: float = 60,
        height: float = 20,
        health: int = 1,
    ) -> Block:
        block = Block(
            id=self._tick(),
            rect=Rectangle(
                left=left,
                top=top,
                width=width,
                height=height,
            ),
            health=health,
        )
        self._state.blocks.append(block)

        return block

    def create_platform(
        self, speed: float, width: float = 120, height: float = 20
    ) -> Platform:
        rect = Rectangle(
            left=0,
            top=0,
            width=width,
            height=height,
        )

        platform = Platform(
            id=self._tick(),
            rect=rect,
            speed=speed,
        )
        self._state.platforms.append(platform)

        return platform

    def create_ball(
        self,
        radius: float,
        speed: float,
        thrown: bool = False,
        top: Optional[float] = None,
        left: Optional[float] = None,
    ) -> Ball:
        ball = Ball(
            id=self._tick(),
            radius=radius,
            thrown=thrown,
            speed=speed,
        )

        if top is not None:
            ball.rect.top = top

        if left is not None:
            ball.rect.left = left

        self._state.balls.append(ball)

        return ball
