from typing import Optional

import pygame as pg

from agym.protocols import IClock


class PygameClock(IClock):
    def __init__(self, target_framerate: float) -> None:
        self._target_framerate = target_framerate
        self._clock = pg.time.Clock()

        # Sould be equal pygame.TIMER_RESOLUTION, but some reason it is 0
        self._timer_resolution = 1000

    def get_framerate(self, percentile: Optional[float] = None) -> float:
        return self._clock.get_fps()

    def do_frame_tick(self) -> float:
        return (
            self._clock.tick(round(self._target_framerate))
            / self._timer_resolution
        )

    @property
    def last_frame_duration(self) -> float:
        return self._clock.get_time() / self._timer_resolution

    def get_global_time(self) -> float:
        return pg.time.get_ticks() / self._timer_resolution
