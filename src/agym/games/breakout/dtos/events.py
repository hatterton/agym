from dataclasses import dataclass, field
from typing import Tuple

from agym.games.breakout.geom import Point
from agym.games.protocols import IGameEvent

from .collisions import Collision


@dataclass
class BreakoutEvent(IGameEvent):
    timestamp: float


@dataclass
class BreakoutCollisionEvent(BreakoutEvent):
    collision: Collision
