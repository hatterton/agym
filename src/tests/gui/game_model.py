from pygame.event import Event

from agym.models import (
    IModel,
)
from agym.games.breakout import (
    BreakoutAction,
)
from agym.interfaces import IEventHandler


class DummyModel(IModel, IEventHandler):
    def __init__(self) -> None:
        self._action = BreakoutAction.NOTHING

    def set_action(self, action: BreakoutAction) -> None:
        self._action = action

    def get_action(self, *args, **kwargs) -> int:
        return self._action.value

    def try_consume_event(self, event: Event) -> bool:
        return False

    def try_delegate_event(self, event: Event) -> bool:
        return False
