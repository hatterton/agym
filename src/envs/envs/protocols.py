from typing import Iterable, Protocol

from geometry import Rectangle, Shape


class IGameItem(Protocol):
    id: int
    rect: Rectangle

    def get_ghost_trace(self, dt: float) -> Iterable[Shape]:
        pass


class IGameState(Protocol):
    def copy(self) -> "IGameState":
        pass

    def get_items(self) -> Iterable[IGameItem]:
        pass


class ILevelBuilder(Protocol):
    def build(self) -> IGameState:
        pass


class IGameAction(Protocol):
    pass


class IGameEvent(Protocol):
    pass


class IGameEnvironment(Protocol):
    @property
    def rect(self) -> Rectangle:
        pass

    @property
    def state(self) -> IGameState:
        pass

    def step(self, action: IGameAction, dt: float) -> bool:
        pass

    def reset(self) -> None:
        pass

    def pop_events(self) -> Iterable[IGameEvent]:
        pass
