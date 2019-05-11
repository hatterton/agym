from enum import Enum
from abc import ABCMeta, ABC, abstractmethod

class IGameEnviroment:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self): raise NotImplementedError

    @abstractmethod
    def reset(self): raise NotImplementedError

    @abstractmethod
    def step(self, action, dt): raise NotImplementedError

    @abstractmethod
    def get_visual_state(self): raise NotImplementedError

    @abstractmethod
    def get_flatten_state(self): raise NotImplementedError

    @abstractmethod
    def blit(self, screen): raise NotImplementedError


