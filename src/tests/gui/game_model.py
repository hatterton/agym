from agym.dtos import Event
from agym.protocols import IEventHandler
from envs.breakout import BreakoutAction, BreakoutActionType
from envs.protocols import IGameState


class DummyModel(IEventHandler):
    def __init__(self) -> None:
        self._action = BreakoutAction(type=BreakoutActionType.NOTHING)

    def set_action(self, action: BreakoutAction) -> None:
        self._action = action

    def get_action(self, state: IGameState) -> BreakoutAction:
        return self._action

    def try_handle_event(self, event: Event) -> bool:
        return False
