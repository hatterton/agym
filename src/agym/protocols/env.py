from typing import Any, List, Protocol, Tuple

from agym.dtos import Event

from .event import IEventHandler


class IGameEnvironment(IEventHandler, Protocol):
    def step(self, action: Any, dt: float) -> Tuple[Any, bool]:
        pass

    def reset(self) -> None:
        pass

    def pop_events(self) -> List[Event]:
        pass
