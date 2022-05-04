from pygame.time import Clock
from agym.utils.queue import Queue
from statistics import mean
from typing import Optional
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

    @profile("get_fps", "fps_update")
    def get_fps(self, percentile: Optional[float] = None) -> float:
        if len(self.ticks) == 0:
            return 0.

        ticks = list(self.ticks)

        ptick: float
        if percentile is None:
            ptick = mean(ticks)
        else:
            assert 0. <= percentile < 1.
            idx = int(percentile * len(ticks))
            ptick = sorted(ticks, reverse=True)[idx]

        return 1. / ptick

    @profile("fps_tick", "game_iter")
    def tick(self) -> int:
        tick = self.clock.tick(self.max_fps)

        self._add_tick(tick / 1000)

        return tick

