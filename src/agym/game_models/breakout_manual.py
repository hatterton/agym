from typing import Tuple

from agym.dtos import Event, KeyboardEvent, KeyCode, KeyDownEvent, KeyUpEvent
from envs.breakout import BreakoutAction, BreakoutActionType
from envs.protocols import IGameState
from agym.protocols import IModel


class ManualBreakoutModel(IModel):
    def __init__(self):
        self._moving_left = False
        self._moving_right = False
        self._promising_throw = False

    def try_handle_event(self, event: Event) -> bool:
        if isinstance(event, KeyDownEvent):
            if event.key.code == KeyCode.LEFT_ARROW:
                self._moving_left = True
                self._moving_right = False
                return True

            elif event.key.code == KeyCode.RIGHT_ARROW:
                self._moving_left = False
                self._moving_right = True
                return True

            elif event.key.code == KeyCode.SPACE:
                self._promising_throw = True
                return True

        elif isinstance(event, KeyUpEvent):
            if event.key.code == KeyCode.LEFT_ARROW:
                self._moving_left = False
                return True

            elif event.key.code == KeyCode.RIGHT_ARROW:
                self._moving_right = False
                return True

        return False

    def get_action(self, state: IGameState) -> BreakoutAction:
        if self._promising_throw:
            self._promising_throw = False
            action_type = BreakoutActionType.THROW

        elif self._moving_right:
            action_type = BreakoutActionType.RIGHT

        elif self._moving_left:
            action_type = BreakoutActionType.LEFT

        else:
            action_type = BreakoutActionType.NOTHING

        return BreakoutAction(type=action_type)
