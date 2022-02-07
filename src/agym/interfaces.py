from abc import ABC, abstractmethod

from pygame.event import Event


class IEventHandler(ABC):
    def try_handle_event(self, event: Event) -> bool:
        performed = False
        if not performed:
            performed = self.try_consume_event(event)

        if not performed:
            performed = self.try_delegate_event(event)

        return performed

    @abstractmethod
    def try_consume_event(self, event: Event) -> bool:
        pass

    @abstractmethod
    def try_delegate_event(self, event: Event) -> bool:
        pass
