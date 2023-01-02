from typing import Iterable, List, Protocol

from envs.protocols import ILevelBuilder

from .dtos import Collision
from .state import BreakoutState


class ICollisionDetector(Protocol):
    def get_step_collisions(
        self, state: BreakoutState, dt: float
    ) -> List[Collision]:
        pass

    def get_time_before_collision(
        self, state: BreakoutState, max_dt: float
    ) -> float:
        pass


class ICollisionDetectorEngine(Protocol):
    def generate_step_collisions(
        self, state: BreakoutState, dt: float
    ) -> Iterable[Collision]:
        pass


class IBreakoutLevelBuilder(ILevelBuilder, Protocol):
    def build(self) -> BreakoutState:
        pass
