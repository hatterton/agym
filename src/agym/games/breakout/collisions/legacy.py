from typing import (
    Iterable,
)

from .dtos import Collision
from .legacy_collision import calculate_colls
from ..state import GameState
from agym.utils import CachedCollection


class LegacyCollisionDetector:
    def generate_step_collisions(self, state: GameState, dt: float) -> Iterable[Collision]:
        return CachedCollection(
            calculate_colls(
                wall_rect=state.wall_rect,
                platforms=state.platforms,
                balls=state.balls,
                blocks=state.blocks,
                dt=dt,
            )
        )
