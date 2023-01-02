from typing import List

from envs.breakout import BreakoutEnv
from envs.breakout import BreakoutEvent, BreakoutState
from envs.breakout.protocols import (
    IBreakoutLevelBuilder,
    ICollisionDetector,
)
from envs.protocols import IGameAction, IGameEnvironment
from geometry import Rectangle, Vec2


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
                env_size=env_size,
                collision_detector=collision_detector,
                level_builder=level_builder,
                checking_gameover=False,
            )
            for _ in range(n)
        ]

    @property
    def state(self) -> BreakoutState:
        return BreakoutState()

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
