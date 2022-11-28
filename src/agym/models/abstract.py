from abc import ABCMeta, abstractmethod
from typing import Tuple


class IModel:
    __metaclass__ = ABCMeta

    def get_action(self, state):
        raise NotImplementedError

    def try_event(self, state):
        raise NotImplementedError


class IQValuesModel(IModel):
    __metaclass__ = ABCMeta

    def get_qvalues(self, states):
        raise NotImplementedError

    def get_t_qvalues(self, t_states):
        raise NotImplementedError

    def parameters(self):
        raise NotImplementedError
