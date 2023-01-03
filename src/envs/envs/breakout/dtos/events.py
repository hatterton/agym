from dataclasses import dataclass

from envs.protocols import IGameEvent

from .collisions import Collision


@dataclass
class BreakoutEvent(IGameEvent):
    timestamp: float


@dataclass
class BreakoutCollisionEvent(BreakoutEvent):
    collision: Collision
