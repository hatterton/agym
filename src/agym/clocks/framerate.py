from typing import Iterable, Optional

from agym.protocols import IClock
from agym.utils.math import lazy_sorted
from custom_queue import IQueue, SizedQueue
from timeprofiler import profile


class FramerateClockDecorator(IClock):
    def __init__(self, clock: IClock, history_size: int = 1000) -> None:
        self._clock = clock
        self._history_size = history_size

        self._ticks: IQueue[float]
        self._reset()

        self._avg_drop: float = 0.5
        self._avg_shift: float = 0.1

        self._perc_drop: float = 0.1
        self._perc_shift: float = 0.005

    def _reset(self) -> None:
        self._ticks = SizedQueue(self._history_size)

    @profile("get_framerate", "game_update")
    def get_framerate(self, percentile: Optional[float] = None) -> float:
        n = len(self._ticks)

        if n == 0:
            return 0.0

        elif n == 1:
            return next(iter(self._ticks))

        ticks = list(self._ticks)
        weights = [self._get_avg_weight(i, n) for i in range(n)]

        if percentile is not None:
            pairs = sorted(zip(ticks, weights), key=lambda x: -x[0])
            weights = [
                self._get_perc_weight(percentile, i, n) for i in range(n)
            ]

            pairs = [(t, w0 * w1) for (t, w0), w1 in zip(pairs, weights)]

            ticks = [t for t, _ in pairs]
            weights = [w for _, w in pairs]

        framerate = sum(weights) / sum(t * w for t, w in zip(ticks, weights))

        return framerate

    def _get_kth_window(self, k: int, window_size: int) -> Iterable[float]:
        window: IQueue[float] = SizedQueue(window_size)

        sorted_ticks = lazy_sorted(self._ticks, key=lambda x: -x)
        for _, tick in zip(range(k), sorted_ticks):
            window.push(tick)

        return window

    def _get_avg_weight(self, idx: int, n: int) -> float:
        x = self._get_coordinate(idx, n)
        w = self._get_weight(
            x=x,
            mx=1.0,
            s=self._avg_shift,
            d=self._avg_drop,
        )

        return w

    def _get_perc_weight(self, perc: float, idx: int, n: int) -> float:
        x = self._get_coordinate(idx, n)
        w = self._get_weight(
            x=x,
            mx=perc,
            s=self._perc_shift,
            d=self._perc_drop,
        )

        return w

    def _get_coordinate(self, idx: int, n: int) -> float:
        return idx / (n - 1)

    def _get_weight(self, x: float, mx: float, s: float, d: float) -> float:
        return d ** (abs(x - mx) / s)

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
