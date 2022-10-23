from typing import (
    Iterable,
)

from .dtos import Collision
from .legacy_collision import calculate_colls
from ..state import GameState
from agym.utils import CachedCollection


class LegacyCollisionDetectorEngine:
    def generate_step_collisions(self, state: GameState, dt: float) -> Iterable[Collision]:
        return CachedCollection(
            calculate_colls(
                walls=state.walls,
                platforms=state.platforms,
                balls=state.balls,
                blocks=state.blocks,
                dt=dt,
            )
        )
