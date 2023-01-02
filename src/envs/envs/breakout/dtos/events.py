from dataclasses import dataclass, field
from typing import Tuple

from envs.protocols import IGameEvent
from geometry import Point

from .collisions import Collision


@dataclass
class BreakoutEvent(IGameEvent):
    timestamp: float


@dataclass
class BreakoutCollisionEvent(BreakoutEvent):
    collision: Collision
