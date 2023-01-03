from agym.protocols import IClock, IUpdater


class LimitedUpdater:
    def __init__(self, updater: IUpdater, clock: IClock, ups: float) -> None:
        self._updater = updater
        self._max_updates_per_second = ups
        self._clock = clock

        self._last_update_time = self._clock.get_global_time()

    def update(self) -> None:
        current_time = self._clock.get_global_time()

        if self._need_update(current_time):
            self._updater.update()
            self._last_update_time = current_time

    def _need_update(self, t: float) -> bool:
        duration = t - self._last_update_time

        return self._max_updates_per_second * duration > 1.0
