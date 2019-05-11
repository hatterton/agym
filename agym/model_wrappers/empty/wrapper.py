from agym.models import (
    IModel,
)
from agym.model_wrappers import (
    IModelWrapper,
)

class EmptyWrapper(IModelWrapper):
    def __init__(self, model: IModel):
        self.model = model

    def get_action(self, state) -> int:
        action = self.model.get_action(state)
        return action

    def post_action(self, next_state, reward: int, is_done: int) -> None:
        pass

    def try_event(self, event) -> bool:
        return self.model.try_event(event)
