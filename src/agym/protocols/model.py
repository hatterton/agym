from typing import Protocol

from agym.games.protocols import IGameAction, IGameState

from .event import IEventHandler


class IModel(IEventHandler, Protocol):
    def get_action(self, state: IGameState) -> IGameAction:
        pass
