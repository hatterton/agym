from pygame.event import Event

from agym.models import (
    IModel,
)
from agym.interfaces import IEventHandler
from agym.model_wrappers import (
    IModelWrapper,
)

class EmptyWrapper(IModelWrapper, IEventHandler):
    def __init__(self, model: IModel):
        self.model = model

    def get_action(self, state) -> int:
        action = self.model.get_action(state)
        return action

    def post_action(self, next_state, reward: int, is_done: int) -> None:
        pass

    def try_consume_event(self, event: Event) -> bool:
        return False

    def try_delegate_event(self, event: Event) -> bool:
        return self.model.try_handle_event(event)
