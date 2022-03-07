import os
import pygame
import enum

from pygame.event import Event
from pygame.mixer import Sound
# import torch
from time import sleep

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
    def __init__(self, width, height, env, model, fps_limiter, fps_label, audio_handler):
        self.screen = pygame.Surface((width, height))

        self.model = model
        self.env = env
        self.fps_limiter = fps_limiter

        self.fps_label = fps_label
        self.audio_handler = audio_handler
        self.run_playing_music()

        self.env.reset()

    def run_playing_music(self) -> None:
        bsound = Sound("agym/static/sounds/death_note_shinigami_kai.mp3")
        bsound.set_volume(0.2)
        # bsound.play(loops=-1)

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
        dt = self.fps_limiter.tick() / 60
        _, is_done = self.env.step(action, dt)

        events = self.env.pop_events()
        self.audio_handler.handle_events(events)

        if is_done:
            self.env.reset()

        self.fps_label.update()

    def blit(self) -> None:
        self.screen.fill((0, 0, 0))
        self.env.blit(self.screen)

        self.fps_label.blit(self.screen)
