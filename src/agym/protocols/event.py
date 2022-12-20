from typing import Protocol

from agym.dtos import PygameEvent


class IEventHandler(Protocol):
    def try_handle_event(self, event: PygameEvent) -> bool:
        pass
