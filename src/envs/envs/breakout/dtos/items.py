from dataclasses import dataclass, field
from typing import Iterable, Optional

from envs.breakout.constants import EPS
from envs.protocols import IGameItem
from geometry import Circle, Point, Rectangle, Shape, Triangle, Vec2

ItemId = int


@dataclass
class Item(IGameItem):
    id: ItemId
    rect: Rectangle

    def get_ghost_trace(self, dt: float) -> Iterable[Shape]:
        return [
            Triangle(
                points=[
                    Point(x=self.rect.left, y=self.rect.top),
                    Point(x=self.rect.right, y=self.rect.top),
                    Point(x=self.rect.left, y=self.rect.bottom),
                ]
            ),
            Triangle(
                points=[
                    Point(x=self.rect.right, y=self.rect.bottom),
                    Point(x=self.rect.right, y=self.rect.top),
                    Point(x=self.rect.left, y=self.rect.bottom),
                ]
            ),
        ]


@dataclass
class Ball(Item):
    radius: float

    thrown: bool
    _velocity: Vec2

    def __init__(
        self,
        id: ItemId,
        radius: float,
        thrown: bool,
        speed: float,
        velocity: Optional[Vec2] = None,
    ) -> None:
        rect = Rectangle(
            left=0,
            top=0,
            width=2 * radius,
            height=2 * radius,
        )

        super().__init__(id=id, rect=rect)

        if velocity is None:
            velocity = Vec2(x=1.0, y=0)

        self.radius = radius
        self.thrown = thrown

        self._velocity: Vec2 = velocity * speed

    @property
    def velocity(self) -> Vec2:
        return self.direction

    @velocity.setter
    def velocity(self, value: Vec2) -> None:
        self.direction = value

    @property
    def direction(self) -> Vec2:
        if self.speed < EPS:
            return Vec2(x=1, y=0)

        return self._velocity / self.speed

    @direction.setter
    def direction(self, value: Vec2) -> None:
        self._velocity = self.speed * value

    @property
    def speed(self) -> float:
        return self._velocity.norm()

    @speed.setter
    def speed(self, value: float) -> None:
        self._velocity = self.direction * value

    def fake_update(self, dt):
        fake_rect = self.rect.copy()
        fake_rect.center += self.velocity * self.speed * dt

        return self.rect.center, fake_rect.center

    def get_ghost_trace(self, dt: float) -> Iterable[Shape]:
        if dt == 0:
            return [
                Circle(
                    center=self.rect.center,
                    radius=self.radius,
                ),
            ]

        vel = self.velocity
        normal_vel = Vec2(x=vel.y, y=-vel.x)
        scaled_normal_vel = normal_vel * self.radius

        start_center = self.rect.center

        shift = vel * self.speed * dt
        finish_center = start_center + shift

        start_p1 = start_center + scaled_normal_vel
        start_p2 = start_center - scaled_normal_vel
        finish_p1 = finish_center + scaled_normal_vel
        finish_p2 = finish_center - scaled_normal_vel

        return [
            Circle(
                center=start_center,
                radius=self.radius,
            ),
            Circle(
                center=finish_center,
                radius=self.radius,
            ),
            Triangle(
                points=[
                    start_p1,
                    start_p2,
                    finish_p1,
                ]
            ),
            Triangle(
                points=[
                    finish_p1,
                    finish_p2,
                    start_p2,
                ]
            ),
        ]


@dataclass
class Block(Item):
    health: int


@dataclass
class Platform(Item):
    speed: float
    velocity: Vec2 = field(default_factory=lambda: Vec2(x=0, y=0))

    rest_freeze_time: float = 0.0
    default_freeze_time: float = 2.0

    def fake_update(self, dt):
        fake_rect = self.rect.copy()

        dt = max(0, dt - self.rest_freeze_time)
        fake_rect.center += self.velocity * self.speed * dt

        return [self.rect, fake_rect]

    def freeze(self):
        self.rest_freeze_time = self.default_freeze_time

    def get_ghost_trace(self, dt: float) -> Iterable[Shape]:
        if dt == 0:
            return super().get_ghost_trace(dt)

        start_rect = self.rect.copy()

        dt = max(0, dt - self.rest_freeze_time)
        finish_rect = self.rect.copy()
        finish_rect.center += self.velocity * self.speed * dt

        left = min(start_rect.left, finish_rect.left)
        right = max(start_rect.right, finish_rect.right)
        top = min(start_rect.top, finish_rect.top)
        bottom = max(start_rect.bottom, finish_rect.bottom)

        return [
            Triangle(
                points=[
                    Point(x=left, y=top),
                    Point(x=right, y=top),
                    Point(x=left, y=bottom),
                ]
            ),
            Triangle(
                points=[
                    Point(x=right, y=bottom),
                    Point(x=right, y=top),
                    Point(x=left, y=bottom),
                ]
            ),
        ]


@dataclass
class Wall(Item):
    pass
