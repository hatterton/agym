from typing import (
    Iterable,
    List,
)

from agym.games.breakout.protocols import ICollisionDetectorEngine
from agym.games.breakout.collisions import Collision
from agym.games.breakout.state import GameState
from agym.games.breakout.constants import EPS

from agym.utils import profile


class CollisionDetector:
    def __init__(self, engine: ICollisionDetectorEngine) -> None:
        self._engine = engine

    @profile("calc_colls", "env_step")
    def get_step_collisions(self, state: GameState, dt: float) -> List[Collision]:
        return list(self._generate_step_collisions(state, dt))

    def _generate_step_collisions(self, state: GameState, dt: float) -> Iterable[Collision]:
        return self._engine.generate_step_collisions(state, dt)

    @profile("calc_time", "env_step")
    def get_time_before_collision(self, state: GameState, max_dt: float) -> float:
        colls = self._generate_step_collisions(state, EPS)
        if any(colls):
            return 0.

        colls = self._generate_step_collisions(state, max_dt)
        if not any(colls):
            return max_dt

        return self._get_time_before_collision(state, max_dt)

    def _get_time_before_collision(self, state: GameState, max_dt: float) -> float:
        min_dt = 0.
        while max_dt - min_dt > EPS:
            mid_dt = (max_dt + min_dt) / 2

            colls = self._engine.generate_step_collisions(state, mid_dt)

            if any(colls):
                max_dt = mid_dt
            else:
                min_dt = mid_dt

        print(min_dt)
        return min_dt
