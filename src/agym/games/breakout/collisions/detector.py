from typing import (
    Iterable,
    List,
    Dict,
)

from agym.games.breakout.protocols import ICollisionDetectorEngine
from agym.games.breakout.collisions import Collision
from agym.games.breakout.state import GameState
from agym.games.breakout.constants import EPS
from agym.games.breakout.items import (
    ItemId,
    Item,
    Ball,
    Block,
    Platform,
)

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
        if any(self._generate_step_collisions(state, EPS)):
            return 0.

        return self._get_time_before_collision(state, max_dt)

    def _get_time_before_collision(self, state: GameState, max_dt: float) -> float:
        colls = self._engine.generate_step_collisions(state, max_dt)
        if not any(colls):
            return max_dt

        state = self._build_collided_state(state, colls)

        min_dt = 0.
        while max_dt - min_dt > EPS:
            mid_dt = (max_dt + min_dt) / 2

            colls = self._engine.generate_step_collisions(state, mid_dt)

            if any(colls):
                max_dt = mid_dt
                state = self._build_collided_state(state, colls)
            else:
                min_dt = mid_dt

        print(min_dt)
        return min_dt

    def _build_collided_state(self, state: GameState, colls: Iterable[Collision]) -> GameState:
        index = self._build_index(state)
        substate = state.duplicate_empty()

        collided_ids = set()
        for coll in colls:
            for item_idx in coll.item_ids:
                collided_ids.add(item_idx)

        for item_idx in collided_ids:
            item = index[item_idx]

            if isinstance(item, Ball):
                substate.balls.append(item)

            elif isinstance(item, Platform):
                substate.platforms.append(item)

            elif isinstance(item, Block):
                substate.blocks.append(item)

        return substate

    def _build_index(self, state: GameState) -> Dict[ItemId, Item]:
        index = dict()
        for ball in state.balls:
            index[ball.id] = ball

        for platform in state.platforms:
            index[platform.id] = platform

        for block in state.blocks:
            index[block.id] = block

        return index
