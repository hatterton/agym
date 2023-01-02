from agym.dtos import Event
from agym.games.breakout.dtos import BreakoutAction, BreakoutActionType
from agym.games.protocols import IGameAction, IGameState
from agym.protocols import IEventHandler


class DummyModel(IEventHandler):
    def __init__(self) -> None:
        self._action = BreakoutAction(type=BreakoutActionType.NOTHING)

    def set_action(self, action: BreakoutAction) -> None:
        self._action = action

    def get_action(self, state: IGameState) -> BreakoutAction:
        return self._action

    def try_handle_event(self, event: Event) -> bool:
        return False
