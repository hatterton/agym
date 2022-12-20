from typing import Protocol


class IUpdater(Protocol):
    def update(self) -> None:
        pass
