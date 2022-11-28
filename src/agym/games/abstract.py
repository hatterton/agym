from abc import ABC, ABCMeta, abstractmethod
from enum import Enum
from typing import Tuple


class IEvent2ActionMapper:
    __metaclass__ = ABCMeta

    def default(self) -> int:
        raise NotImplementedError

    def map(self, event) -> Tuple[bool, int]:
        raise NotImplementedError


class IGameEnviroment:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        raise NotImplementedError

    @abstractmethod
    def step(self, action, dt):
        raise NotImplementedError

    @abstractmethod
    def blit(self, screen):
        raise NotImplementedError
