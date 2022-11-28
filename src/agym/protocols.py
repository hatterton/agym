from typing import Any, List, Protocol, Tuple

from .dtos import Event, PygameEvent


class IUpdater(Protocol):
    def update(self) -> None:
        pass


class IEventHandler(Protocol):
    def try_handle_event(self, event: PygameEvent) -> bool:
        pass


class IModel(IEventHandler, Protocol):
    def get_action(self, state) -> int:
        pass


class IGameEnvironment(IEventHandler, Protocol):
    def step(self, action: Any, dt: float) -> Tuple[Any, bool]:
        pass

    def reset(self) -> None:
        pass

    def pop_events(self) -> List[Event]:
        pass

    def blit(self, screen) -> None:
        pass
