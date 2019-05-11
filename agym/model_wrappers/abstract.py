from abc import ABCMeta, abstractmethod

class IModelWrapper:
    @abstractmethod
    def get_action(self, state): raise NotImplementedError

    @abstractmethod
    def post_action(self, next_state, reward, is_done):
        raise NotImplementedError

    @abstractmethod
    def try_event(self, event): raise NotImplementedError

