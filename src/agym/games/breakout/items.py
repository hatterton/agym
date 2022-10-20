import pygame
import os
from typing import Iterable

from abc import ABC, abstractmethod
from pygame.sprite import Sprite
from agym.games.breakout.geom import (
    Shape,
    Circle,
    Rectangle,
    Triangle,
    Point,
    Vec2,
)

ItemId = int


class Item(ABC, Sprite):
    def __init__(self, image_name: str, item_id: ItemId):
        super(Item, self).__init__()
        image_path = os.path.join(
            "agym/static/images/breakout",
            image_name,
        )
        self.image = pygame.image.load(image_path)
        self.id = item_id

        self.rect = Rectangle.from_rect(self.image.get_rect())

    def blit(self, screen) -> None:
        rect = self.image.get_rect().move(self.rect.left, self.rect.top)
        screen.blit(self.image, rect)

    @abstractmethod
    def get_ghost_trace(self, dt: float) -> Iterable[Shape]:
        raise NotImplemented


class Block(Item):
    def __init__(self, image_name: str, top: int, left: int, health: int, item_id: ItemId):
        super(Block, self).__init__(image_name, item_id)
        self.rect.top = top
        self.rect.left = left

        self.health = health

    def get_ghost_trace(self, dt: float) -> Iterable[Shape]:
        # return [self.rect.copy()]
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


class Platform(Item):
    def __init__(self, image_name: str, speed: float, item_id: ItemId):
        super(Platform, self).__init__(image_name, item_id)

        self.speed: float = speed
        self.velocity: Vec2 = Vec2(x=0, y=0)

        self.rest_freeze_time = 0
        self.default_freeze_time = 2

    def fake_update(self, dt):
        fake_rect = self.rect.copy()

        if self.rest_freeze_time <= dt:
            dt -= self.rest_freeze_time
            fake_rect.center += self.velocity * self.speed * dt

        return [self.rect, fake_rect]

    def freeze(self):
        self.rest_freeze_time = self.default_freeze_time

    def get_ghost_trace(self, dt: float) -> Iterable[Shape]:
        start_rect = self.rect.copy()

        dt = max(0, dt - self.rest_freeze_time)
        finish_rect = self.rect.copy()
        finish_rect.center += self.velocity * self.speed * dt

        # TODO it is not valid ghost trace
        return [
            Triangle(
                points=[
                    Point(x=start_rect.left, y=start_rect.top),
                    Point(x=start_rect.right, y=start_rect.top),
                    Point(x=start_rect.left, y=start_rect.bottom),
                ]
            ),
            Triangle(
                points=[
                    Point(x=start_rect.right, y=start_rect.bottom),
                    Point(x=start_rect.right, y=start_rect.top),
                    Point(x=start_rect.left, y=start_rect.bottom),
                ]
            ),
            Triangle(
                points=[
                    Point(x=finish_rect.left, y=finish_rect.top),
                    Point(x=finish_rect.right, y=finish_rect.top),
                    Point(x=finish_rect.left, y=finish_rect.bottom),
                ]
            ),
            Triangle(
                points=[
                    Point(x=finish_rect.right, y=finish_rect.bottom),
                    Point(x=finish_rect.right, y=finish_rect.top),
                    Point(x=finish_rect.left, y=finish_rect.bottom),
                ]
            ),
        ]


class Ball(Item):
    def __init__(self, image_name, radius, speed, thrown: bool, item_id: ItemId):
        super(Ball, self).__init__(image_name, item_id)

        self.radius = radius
        self.color_cirle = pygame.Color(0, 0, 0)

        self.thrown = thrown
        self.velocity: Vec2 = Vec2(x=0, y=0)
        self.speed = speed

    def fake_update(self, dt):
        fake_rect = self.rect.copy()
        fake_rect.center += self.velocity * self.speed * dt

        return self.rect.center, fake_rect.center

    def get_ghost_trace(self, dt: float) -> Iterable[Shape]:
        vel = self.velocity
        normal_vel = Vec2(x=vel.y, y=-vel.x)
        scaled_normal_vel = normal_vel * self.radius
        # scaled_normal_vel = normal_vel * self.speed * dt

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

