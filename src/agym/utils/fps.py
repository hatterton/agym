from statistics import mean
from typing import Optional

from pygame.time import Clock

from agym.constants import TIME_RESOLUTION
from agym.utils.math import get_n_max
from agym.utils.queue import Queue
from agym.utils.timemanager import profile


class FPSLimiter:
    def __init__(self, max_fps: int, history_size: int = 100):
        self.max_fps = max_fps
        self.history_size = history_size

        self.clock: Clock
        self.ticks: Queue[float]

        self.reset()

    def reset(self) -> None:
        self.clock = Clock()
        self.ticks = Queue()

    def _add_tick(self, tick: float) -> None:
        self.ticks.push(tick)
        if len(self.ticks) > self.history_size:
            self.ticks.pop()

    @profile("get_fps", "game_update")
    def get_fps(self, percentile: Optional[float] = None) -> float:
        if len(self.ticks) == 0:
            return 0.0

        ticks = list(self.ticks)

        ptick: float
        if percentile is None:
            ptick = mean(ticks)
        else:
            assert 0.0 <= percentile < 1.0

            idx = max(1, int(percentile * len(ticks)))
            ptick = mean(get_n_max(ticks, n=idx))

        return TIME_RESOLUTION / ptick

    @profile("game_sleep", "game_update")
    def tick(self) -> float:
        tick = self.clock.tick(self.max_fps)

        self._add_tick(tick)

        return tick
