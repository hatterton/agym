from typing import Tuple

import pygame
from pygame.event import Event

from agym.games.breakout.dtos import BreakoutAction, BreakoutActionType
from agym.games.protocols import IGameState


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

    def get_action(self, state: IGameState) -> BreakoutAction:
        if self.promise_throw:
            self.promise_throw = False
            action_type = BreakoutActionType.THROW

        elif self.platform_moving_right:
            action_type = BreakoutActionType.RIGHT

        elif self.platform_moving_left:
            action_type = BreakoutActionType.LEFT

        else:
            action_type = BreakoutActionType.NOTHING

        return BreakoutAction(type=action_type)
