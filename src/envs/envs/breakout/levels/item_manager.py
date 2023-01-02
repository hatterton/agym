import random
from typing import List, Optional

from envs.breakout.dtos import Ball, Block, Platform, Wall
from envs.breakout.state import BreakoutState
from geometry import Rectangle


class ItemManager:
    def __init__(self) -> None:
        self._item_counter = 0

        self._state: BreakoutState
        self._reset()

    def _tick(self) -> int:
        res = self._item_counter
        self._item_counter += 1

        return res

    def _reset(self) -> None:
        self._state = BreakoutState()

    def extract_state(self) -> BreakoutState:
        res = self._state
        self._reset()

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
