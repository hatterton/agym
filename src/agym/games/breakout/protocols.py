from typing import Iterable, List, Protocol

from agym.games.protocols import ILevelBuilder

from .dtos import Collision
from .state import GameState


class ICollisionDetector(Protocol):
    def get_step_collisions(
        self, state: GameState, dt: float
    ) -> List[Collision]:
        pass

    def get_time_before_collision(
        self, state: GameState, max_dt: float
    ) -> float:
        pass


class ICollisionDetectorEngine(Protocol):
    def generate_step_collisions(
        self, state: GameState, dt: float
    ) -> Iterable[Collision]:
        pass


class IBreakoutLevelBuilder(ILevelBuilder, Protocol):
    def build(self) -> GameState:
        pass
