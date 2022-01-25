import time
import pygame
from pygame.time import Clock

class FPSLimiter:
    def __init__(self, max_fps):
        self.max_fps = max_fps
        self.cicle_time = 1000 // max_fps

        self.reset()

    def reset(self):
        # self.last_tick = pygame.time.get_ticks()

        self.clock = Clock()

    def cicle(self):
        self.clock.tick(self.max_fps)
        print(self.clock.get_fps())
        return self.clock.get_time()


        current_tick = pygame.time.get_ticks()
        dt = current_tick - self.last_tick

        if dt < self.cicle_time:
            extra_dt = pygame.time.wait(self.cicle_time - dt)
            dt += extra_dt

        self.last_tick += dt

        return dt

