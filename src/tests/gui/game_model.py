from pygame.event import Event

from agym.games.breakout import BreakoutAction


class DummyModel:
    def __init__(self) -> None:
        self._action = BreakoutAction.NOTHING

    def set_action(self, action: BreakoutAction) -> None:
        self._action = action

    def get_action(self, *args, **kwargs) -> int:
        return self._action.value

    def try_handle_event(self, event: Event) -> bool:
        return False
