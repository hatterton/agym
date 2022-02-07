import pygame
from pygame.event import Event

from agym.models import (
    IModel,
)

from agym.interfaces import IEventHandler
from agym.games.breakout.env import (
    BreakoutAction,
)

from typing import (
    Tuple,
)

class ManualBreakoutModel(IModel, IEventHandler):
    def __init__(self):
        self.platform_moving_left = False
        self.platform_moving_right = False
        self.promise_throw = False

    def try_consume_event(self, event: Event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.platform_moving_left = True
                self.platform_moving_right = False
            elif event.key == pygame.K_RIGHT:
                self.platform_moving_left = False
                self.platform_moving_right = True
            elif event.key == pygame.K_SPACE:
                self.promise_throw = True
            else:
                return False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.platform_moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.platform_moving_right = False
            else:
                return False
        else:
            return False

        return True

    def try_delegate_event(self, event: Event) -> bool:
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
