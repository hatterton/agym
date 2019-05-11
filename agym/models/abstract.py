from abc import ABCMeta, abstractmethod
from typing import Tuple

class IEvent2ActionMapper:
    __metaclass__ = ABCMeta

    def map(self, event) -> Tuple[bool, int]: raise NotImplementedError

class IModel:
    __metaclass__ = ABCMeta

    def get_action(self, state): raise NotImplementedError

    def try_event(self, state): raise NotImplementedError

