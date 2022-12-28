from typing import List

from agym.games import BreakoutEnv
from agym.games.breakout import BreakoutEvent, GameState
from agym.games.breakout.geom import Rectangle, Vec2
from agym.games.breakout.protocols import (
    IBreakoutLevelBuilder,
    ICollisionDetector,
)
from agym.games.protocols import IGameAction, IGameEnvironment


class ManyBreakoutsEnv(IGameEnvironment):
    def __init__(
        self,
        n: int,
        env_size: Vec2,
        collision_detector: ICollisionDetector,
        level_builder: IBreakoutLevelBuilder,
    ) -> None:
        self._env_rect = Rectangle(
            left=0,
            top=0,
            width=env_size.x,
            height=env_size.y,
        )

        self.envs = [
            BreakoutEnv(
                env_width=env_size.x,
                env_height=env_size.y,
                collision_detector=collision_detector,
                level_builder=level_builder,
                checking_gameover=False,
            )
            for _ in range(n)
        ]

    @property
    def state(self) -> GameState:
        return GameState()

    @property
    def rect(self) -> Rectangle:
        return self._env_rect

    def step(self, action: IGameAction, dt: float) -> bool:
        for env in self.envs:
            env.step(action, dt)

        return False

    def reset(self) -> None:
        for env in self.envs:
            env.reset()

    def pop_events(self) -> List[BreakoutEvent]:
        events = []
        for env in self.envs:
            events += env.pop_events()

        return events
