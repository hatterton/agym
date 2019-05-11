import pygame
import os
import random
import copy

from pygame.sprite import Sprite


class Item(Sprite):
    def __init__(self, image_name: str):
        super(Item, self).__init__()
        image_path = os.path.join(
            "agym/games/breakout/static/images",
            image_name,
        )
        # print(image_path)
        self.image = pygame.image.load(image_path)

        self.rect = self.image.get_rect()
        self.center = (float(self.rect.centerx), float(self.rect.centery))

    def get_rect(self):
        return self.rect

    def sync(self) -> None:
        self.rect.centerx = int(self.center[0])
        self.rect.centery = int(self.center[1])

    def blit(self, screen) -> None:
        screen.blit(self.image, self.rect)


class Block(Item):
    def __init__(self, image_name: str, top: int, left: int):
        super(Block, self).__init__(image_name)
        self.rect.top = top
        self.rect.left = left

    # def make_intersected(self, arg):
    #     sel1 = agym.param.left_side < self.rect.right
    #     sel2 = agym.param.right_side > self.rect.left
    #     sel3 = np.logical_and(sel1, sel2)
    #     sel4 = agym.param.top_side < self.rect.bottom
    #     sel5 = agym.param.bottom_side > self.rect.top
    #     sel6 = np.logical_and(sel4, sel5)

    #     sel7 = np.logical_and(sel3[np.newaxis, :], sel6[:, np.newaxis])
    #     self.intersected = np.transpose(sel7)


class Platform(Item):
    def __init__(self, image_name, velocity):
        super(Platform, self).__init__(image_name)

        self.moving_right = False
        self.moving_left = False

        self.velocity = velocity

        self.rest_freeze_time = 0
        self.default_freeze_time = 2

    def fake_update(self, dt):
        result = copy.copy(self.rect)
        fake_center = copy.copy(self.center)

        if self.rest_freeze_time <= dt:
            dt -= self.rest_freeze_time
            if self.moving_right:
                fake_center[0] += self.velocity * dt
            elif self.moving_left:
                fake_center[0] -= self.velocity * dt

        result.centerx = int(fake_center[0])
        result.centery = int(fake_center[1])
        return [self.rect, result]


    def update(self, dt):
        if self.rest_freeze_time <= dt:
            dt -= self.rest_freeze_time
            if self.moving_right:
                fake_center[0] += self.velocity * dt
            elif self.moving_left:
                fake_center[0] -= self.velocity * dt

        self.rest_freeze_time = max(0, self.rest_freeze_time - dt)

        # if self.rect.left < 0:
        #     self.center[0] -= self.rect.left
        # if self.rect.right > self.area_rect.width:
        #     self.center[0] += self.area_rect.width - self.rect.right

        self.sync()

    def freeze(self):
        self.rest_freeze_time = self.default_freeze_time

    # def restart(self, arg):
    #     self.rect.top = arg.settings.ga_height - self.rect.height - 10
    #     self.rect.centerx = self.screen_rect.width // 2
    #     self.center = list(map(float, [self.rect.centerx, self.rect.centery]))



class Ball(Item):
    def __init__(self, image_name, radius, velocity):
        super(Ball, self).__init__(image_name)

        self.radius = radius + 2
        self.color_cirle = pygame.Color(0, 0, 0)

        self.thrown = False
        self.vec_velocity = [0, 0]
        self.velocity = velocity


    def fake_update(self, alpha):
        # TODO
        result = copy.copy(self.rect)
        fake_center = copy.copy(self.center)

        if not self.thrown:
            result.bottom = self.platform.rect.top
            result.centerx = self.platform.rect.centerx
            fake_center = list(map(float, [self.rect.centerx, self.rect.centery]))
        else:
            for i in range(2):
                fake_center[i] += self.velocity[i] * self.alpha_velocity * alpha
        
        result.centerx, result.centery = [int(item) for item in fake_center]
        return [self.center, fake_center, self.radius]

    def update(self, alpha):
        # TODO
        # if alpha != 1.0:
        #     print("Ball {}".format(alpha))

        if not self.thrown:
            self.rect.bottom = self.platform.rect.top
            self.rect.centerx = self.platform.rect.centerx
            self.center = list(map(float, [self.rect.centerx, self.rect.centery]))
        else:
            for i in range(2):
                self.center[i] += self.velocity[i] * self.alpha_velocity * alpha

        self.sync()

    def move_on_platform(self, rect) -> None:
        self.thrown = False
        self.rect.bottom = rect.top
        self.rect.centerx = rect.centerx

    def throw(self) -> None:
        if not self.thrown:
            self.thrown = True
            miss = random.random() - 0.5
            self.velocity = [miss*4, -1]
            v_mod = sum(self.velocity[i]**2 for i in range(2))**0.5
            self.velocity = [self.velocity[i]/v_mod for i in range(2)]

            self.rect.bottom = self.platform.rect.top - 2

