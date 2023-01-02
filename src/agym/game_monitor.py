import enum
import os
from time import sleep

from pygame.mixer import Sound

from agym.constants import TIME_RESOLUTION
from agym.dtos import Event
from agym.games.protocols import IGameEnvironment
from agym.gui import TextLabel
from agym.protocols import IClock, IEventHandler, IModel
from agym.utils import profile


class GameMonitor(IEventHandler):
    def __init__(
        self,
        env: IGameEnvironment,
        model: IModel,
        clock: IClock,
        fps_label: TextLabel,
        profile_label: TextLabel,
        log_updater,
        audio_handler,
        tps: int,
    ):
        self.model = model
        self.env = env
        self._clock = clock

        self.fps_label = fps_label
        self.profile_label = profile_label

        self.log_updater = log_updater

        self.audio_handler = audio_handler
        # self.run_playing_music()

        self.tps = tps

        self.env.reset()

    def run_playing_music(self) -> None:
        bsound = Sound(
            "../static/envs/breakout/sounds/death_note_shinigami_kai.mp3"
        )
        bsound.set_volume(0.2)
        bsound.play(loops=-1)

    @profile("game_event")
    def try_handle_event(self, event: Event) -> bool:
        handled = False
        handled = handled or self.model.try_handle_event(event)

        return handled

    @profile("game_update")
    def update(self) -> None:
        state = self.env.state

        action = self.model.get_action(state)

        dt = self._clock.do_frame_tick() * self.tps
        is_done = self.env.step(action, dt)

        events = self.env.pop_events()
        self.audio_handler.handle_events(events)

        if is_done:
            self.env.reset()

        self.log_updater.update()
