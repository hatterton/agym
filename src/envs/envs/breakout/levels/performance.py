import random
from typing import List

from envs.breakout.dtos import Wall
from envs.breakout.protocols import ILevelBuilder
from envs.breakout.state import BreakoutState
from geometry import Rectangle, Vec2

from .item_manager import ItemManager


class PerformanceLevelBuilder(ILevelBuilder):
    def __init__(
        self,
        env_size: Vec2,
        num_balls: int,
        ball_radius: float,
        ball_speed: float,
    ) -> None:
        self._item_manager = ItemManager()

        self._env_size = env_size

        self._num_balls = num_balls
        self._ball_radius = ball_radius
        self._ball_speed = ball_speed

    def build(self) -> BreakoutState:
        self._make_walls()
        self._make_balls()

        return self._item_manager.extract_state()

    def _make_walls(self) -> List[Wall]:
        shift = 5.0
        left = shift
        top = shift
        right = self._env_size.x - shift
        bottom = self._env_size.x - shift

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
            self._item_manager.create_wall(left_wall),
            self._item_manager.create_wall(top_wall),
            self._item_manager.create_wall(right_wall),
            self._item_manager.create_wall(bottom_wall),
        ]

    def _make_balls(
        self,
    ):
        n_balls = self._num_balls
        radius = self._ball_radius
        ball_speed = self._ball_speed

        n = 1
        while n**2 < n_balls:
            n += 1

        velocities = [
            [i / (i**2 + j**2) ** 0.5, j / (i**2 + j**2) ** 0.5]
            for i in range(-10, 10)
            for j in range(-10, 10)
            if i != 0 or j != 0
        ]

        balls = []
        for i in range(n_balls):
            row = i // n
            col = i % n

            ball = self._item_manager.create_ball(
                radius=radius,
                speed=ball_speed,
                thrown=True,
            )

            ball.rect.centerx = (col + 1) * self._env_size.x / (n + 1)
            ball.rect.centery = (row + 1) * self._env_size.y / (n + 1)

            velocity = random.choice(velocities).copy()
            ball.velocity = Vec2.from_list(velocity)

            balls.append(ball)

        return balls
