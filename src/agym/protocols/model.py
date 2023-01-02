from typing import Protocol

from envs.protocols import IGameAction, IGameState

from .event import IEventHandler


class IModel(IEventHandler, Protocol):
    def get_action(self, state: IGameState) -> IGameAction:
        pass
