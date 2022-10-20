from typing import (
    Protocol,
    Iterable,
    List,
)

from .collisions import Collision
from .state import GameState
from .levels import Level


class ICollisionDetector(Protocol):
    def get_step_collisions(self, state: GameState, dt: float) -> List[Collision]:
        pass

    def get_time_before_collision(self, state: GameState, max_dt: float) -> float:
        pass


class ICollisionDetectorEngine(Protocol):
    def generate_step_collisions(self, state: GameState, dt: float) -> Iterable[Collision]:
        pass


class ILevelBuilder(Protocol):
    def build(self) -> Level:
        pass
