from typing import Iterable, Protocol

from agym.dtos import Event


class IEventHandler(Protocol):
    def try_handle_event(self, event: Event) -> bool:
        pass


class IEventSource(Protocol):
    def get_events(self) -> Iterable[Event]:
        pass
