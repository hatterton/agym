import pygame
import os
from typing import List

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


class Item(Sprite):
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


class Block(Item):
    def __init__(self, image_name: str, top: int, left: int, health: int, item_id: ItemId):
        super(Block, self).__init__(image_name, item_id)
        self.rect.top = top
        self.rect.left = left

        self.health = health

    def get_ghost_trace(self, dt) -> List[Shape]:
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
        fake_rect = Rectangle.from_rect(self.rect)

        if self.rest_freeze_time <= dt:
            dt -= self.rest_freeze_time
            fake_rect.center += self.velocity * self.speed * dt

        return [self.rect, fake_rect]

    def freeze(self):
        self.rest_freeze_time = self.default_freeze_time

    def get_ghost_trace(self, dt) -> List[Shape]:
        # TODO it is not valid ghost trace
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


class Ball(Item):
    def __init__(self, image_name, radius, speed, thrown: bool, item_id: ItemId):
        super(Ball, self).__init__(image_name, item_id)

        self.radius = radius
        self.color_cirle = pygame.Color(0, 0, 0)

        self.thrown = thrown
        self.velocity: Vec2 = Vec2(x=0, y=0)
        self.speed = speed

    def fake_update(self, dt):
        fake_rect = Rectangle.from_rect(self.rect)
        fake_rect.center += self.velocity * self.speed * dt

        return self.rect.center, fake_rect.center

    def get_ghost_trace(self, dt) -> List[Shape]:
        s = self.speed * dt

        vel = Vec2(x=self.velocity[0], y=self.velocity[1])
        normal_vel = Vec2(x=vel.y, y=-vel.x)
        scaled_normal_vel = normal_vel * s

        start_center = Point(x=self.rect.centerx, y=self.rect.centery)
        shift = vel * s
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

