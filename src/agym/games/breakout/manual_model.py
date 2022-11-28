from typing import Tuple

import pygame
from pygame.event import Event

from agym.games.breakout.env import BreakoutAction


class ManualBreakoutModel:
    def __init__(self):
        self.platform_moving_left = False
        self.platform_moving_right = False
        self.promise_throw = False

    def try_handle_event(self, event: Event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.platform_moving_left = True
                self.platform_moving_right = False
                return True

            elif event.key == pygame.K_RIGHT:
                self.platform_moving_left = False
                self.platform_moving_right = True
                return True

            elif event.key == pygame.K_SPACE:
                self.promise_throw = True
                return True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.platform_moving_left = False
                return True

            elif event.key == pygame.K_RIGHT:
                self.platform_moving_right = False
                return True

        return False

    def get_action(self, state) -> int:
        if self.promise_throw:
            self.promise_throw = False
            return BreakoutAction.THROW.value
        elif self.platform_moving_right:
            return BreakoutAction.RIGHT.value
        elif self.platform_moving_left:
            return BreakoutAction.LEFT.value

        return BreakoutAction.NOTHING.value
