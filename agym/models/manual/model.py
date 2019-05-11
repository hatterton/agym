from agym.models import (
    IEvent2ActionMapper,
    IModel,
)
from typing import Tuple

class DefaultMapper(IEvent2ActionMapper):
    def __init__(self):
        pass

    def map(self, event) -> Tuple[bool, int]:
        return False, -1

class ManualControlModel(IModel):
    def __init__(self,
                 event2action_mapper: IEvent2ActionMapper = None):
        if event2action_mapper is None:
            self.mapper = DefaultMapper()
        else:
            self.mapper = event2action_mapper

    def try_event(self, event) -> bool:
        code, self.action = self.mapper.map(event)
        return code

    def get_action(self, state) -> int:
        return self.action
