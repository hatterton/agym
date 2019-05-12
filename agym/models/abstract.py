from abc import ABCMeta, abstractmethod
from typing import Tuple


class IModel:
    __metaclass__ = ABCMeta

    def get_action(self, state): raise NotImplementedError

    def try_event(self, state): raise NotImplementedError

