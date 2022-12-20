from typing import Iterable, Optional

from agym.protocols import IClock
from agym.utils.math import lazy_sorted
from agym.utils.queue import IQueue, SizedQueue
from agym.utils.timemanager import profile


class FramerateClockDecorator(IClock):
    def __init__(self, clock: IClock, history_size: int = 1000) -> None:
        self._clock = clock
        self._history_size = history_size

        self._ticks: IQueue[float]
        self._reset()

    def _reset(self) -> None:
        self._ticks = SizedQueue(self._history_size)

    @profile("get_framerate", "game_update")
    def get_framerate(self, percentile: Optional[float] = None) -> float:
        if len(self._ticks) == 0:
            return 0.0

        if percentile is None:
            ticks = list(self._ticks)

        else:
            n = len(self._ticks)
            k: int = max(1, min(round(percentile * n), n))

            ticks = list(self._get_kth_window(k, window_size=3))

        framerate = len(ticks) / sum(ticks)

        return framerate

    def _get_kth_window(self, k: int, window_size: int) -> Iterable[float]:
        window: IQueue[float] = SizedQueue(window_size)

        sorted_ticks = lazy_sorted(self._ticks, key=lambda x: -x)
        for _, tick in zip(range(k), sorted_ticks):
            window.push(tick)

        return window

    @profile("game_sleep", "game_update")
    def do_frame_tick(self) -> float:
        tick_duration = self._clock.do_frame_tick()

        self._add_tick(tick_duration)

        return tick_duration

    def _add_tick(self, tick: float) -> None:
        self._ticks.push(tick)

    @property
    def last_frame_duration(self) -> float:
        return self._ticks.front

    def get_global_time(self) -> float:
        return self._clock.get_global_time()
