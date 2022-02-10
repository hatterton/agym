import pygame
import os
import random
import copy

from pygame.sprite import Sprite
from agym.games.breakout.custom_rect import Rect


class Item(Sprite):
    def __init__(self, image_name: str):
        super(Item, self).__init__()
        image_path = os.path.join(
            "agym/static/images/breakout",
            image_name,
        )
        self.image = pygame.image.load(image_path)

        self.rect = Rect(self.image.get_rect())

    def blit(self, screen) -> None:
        screen.blit(self.image, self.rect.as_rect())


class Block(Item):
    def __init__(self, image_name: str, top: int, left: int):
        super(Block, self).__init__(image_name)
        self.rect.top = top
        self.rect.left = left


class Platform(Item):
    def __init__(self, image_name, velocity):
        super(Platform, self).__init__(image_name)

        self.velocity = velocity
        self.vec_velocity = [0, 0]

        self.rest_freeze_time = 0
        self.default_freeze_time = 2

    def fake_update(self, dt):
        fake_rect = self.rect.copy()

        if self.rest_freeze_time <= dt:
            dt -= self.rest_freeze_time
            fake_rect.center[0] += (self.velocity * dt *
                                    self.vec_velocity[0])

        return [self.rect, fake_rect]

    def freeze(self):
        self.rest_freeze_time = self.default_freeze_time


class Ball(Item):
    def __init__(self, image_name, radius, velocity):
        super(Ball, self).__init__(image_name)

        self.radius = radius
        self.color_cirle = pygame.Color(0, 0, 0)

        self.thrown = False
        self.vec_velocity = [0, 0]
        self.velocity = velocity


    def fake_update(self, dt):
        fake_rect = self.rect.copy()

        for i in range(2):
            fake_rect.center[i] += (self.velocity *
                                    self.vec_velocity[i] * dt)

        return self.rect.center, fake_rect.center

