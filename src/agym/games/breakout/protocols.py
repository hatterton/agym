from typing import (
    Protocol,
    Iterable,
)

from .collisions import Collision
from .state import GameState


class ICollisionDetector(Protocol):
    def generate_step_collisions(self, state: GameState, dt: float) -> Iterable[Collision]:
        pass
