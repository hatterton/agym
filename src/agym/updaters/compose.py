from typing import List

from agym.protocols import IUpdater


class ComposeUpdater:
    def __init__(self, updaters: List[IUpdater]) -> None:
        self._updaters = updaters

    def update(self) -> None:
        for updater in self._updaters:
            updater.update()
