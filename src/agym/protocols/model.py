from typing import Protocol

from .event import IEventHandler


class IModel(IEventHandler, Protocol):
    def get_action(self, state) -> int:
        pass
