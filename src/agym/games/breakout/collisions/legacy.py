from typing import (
    Iterable,
)

from .dtos import Collision
from .legacy_collision import calculate_colls
from ..state import GameState


class LegacyCollisionDetector:
    def generate_step_collisions(self, state: GameState, dt: float) -> Iterable[Collision]:
        return calculate_colls(
            wall_rect=state.wall_rect,
            platform=state.platforms[0],
            ball= state.balls[0],
            blocks=state.blocks,
            dt=dt,
        )
