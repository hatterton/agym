from pygame.time import get_ticks

from agym.utils import TimeProfiler, format_stats
from agym.gui import TextLabel
from agym.protocols import IUpdater
from agym.constants import TIME_RESOLUTION


class LimitedUpdater:
    def __init__(self, updater: IUpdater, ups: float) -> None:
        self.updater = updater
        self.max_ups = ups

        self.last_update = get_ticks()

    def update(self) -> None:
        t = get_ticks()

        if self._need_update(t):
            self.updater.update()
            self.last_update = t

    def _need_update(self, t: int) -> bool:
        duration = t - self.last_update

        return self.max_ups * duration > TIME_RESOLUTION

