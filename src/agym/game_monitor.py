import os
import pygame
import enum

from pygame.event import Event
# import torch

# from agym.gui import Menu
# from agym.config import Config
# from agym.models import (
#     IModel,
    # ConvQValuesModel,
# )
from agym.interfaces import IEventHandler
from agym.model_wrappers import (
    # IModelWrapper,
    EmptyWrapper,
    # SarsaWrapper,
)
from agym.games import (
    IGameEnviroment,
)
# from agym.gui.menu import (
#     # IMenu,
#     Menu,
# )


class GameMonitor(IEventHandler):
    def __init__(self, width, height, env, model, fps_limiter):
        self.screen = pygame.Surface((width, height))

        self.model = model
        self.env = env
        self.fps_limiter = fps_limiter

        self.env.reset()

    def try_consume_event(self, event: Event) -> bool:
        return False

    def try_delegate_event(self, event: Event) -> bool:
        delegated = False

        if not delegated:
            delegated = self.model.try_handle_event(event)

        if not delegated:
            delegated = self.env.try_handle_event(event)

        return delegated

    def update(self) -> None:
        action = self.model.get_action(None)
        dt = self.fps_limiter.cicle() / 60
        _, is_done = self.env.step(action, dt)

        if is_done:
            self.env.reset()
            self.fps_limiter.reset()

    def blit(self) -> None:
        self.screen.fill((0, 0, 0))
        self.env.blit(self.screen)

        # self.screen.blit(self.env.screen, self.env_rect)
