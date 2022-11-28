from typing import Protocol

from .dtos import Event


class IUpdater(Protocol):
    def update(self) -> None:
        pass


class IEventHandler(Protocol):
    def try_handle_event(self, event: Event) -> bool:
        pass


class IModel(IEventHandler):
    def get_action(self, state):
        pass


class IGameEnvironment(IUpdater):
    def step(self, state, action):
        pass

    def blit(self, screen) -> None:
        pass
