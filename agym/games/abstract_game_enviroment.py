from abc import ABC, abstractmethod

class AbstractGameEnviroment(ABC):

    def __init__(self):
        super(self, ABC).__init__()

    @abstractmethod
    def reset(self):
        pass

    @abstract
    def step(self):
        pass


