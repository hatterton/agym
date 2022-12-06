import enum
import os
from time import sleep

import pygame
from pygame.event import Event
from pygame.mixer import Sound

from agym.constants import TIME_RESOLUTION
from agym.gui import TextLabel
from agym.protocols import IEventHandler, IGameEnvironment, IModel
from agym.utils import profile


class GameMonitor:
    def __init__(
        self,
        width: int,
        height: int,
        env: IGameEnvironment,
        model: IModel,
        fps_limiter,
        fps_label: TextLabel,
        profile_label: TextLabel,
        log_updater,
        audio_handler,
        tps: int,
    ):
        self.model = model
        self.env = env
        self.fps_limiter = fps_limiter

        self.fps_label = fps_label
        self.profile_label = profile_label

        self.log_updater = log_updater

        self.audio_handler = audio_handler
        # self.run_playing_music()

        self.tps = tps

        self.env.reset()

    def run_playing_music(self) -> None:
        bsound = Sound("agym/static/sounds/death_note_shinigami_kai.mp3")
        bsound.set_volume(0.2)
        bsound.play(loops=-1)

    @profile("game_event")
    def try_handle_event(self, event: Event) -> bool:
        handled = False
        handled = handled or self.model.try_handle_event(event)
        handled = handled or self.env.try_handle_event(event)

        return handled

    @profile("game_update")
    def update(self) -> None:
        action = self.model.get_action(None)
        dt = self.fps_limiter.tick() * self.tps / TIME_RESOLUTION
        _, is_done = self.env.step(action, dt)

        events = self.env.pop_events()
        self.audio_handler.handle_events(events)

        if is_done:
            self.env.reset()

        self.log_updater.update()
