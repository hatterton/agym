from dataclasses import dataclass, field
from typing import Tuple

from .geom import Point
from .collisions import Collision


@dataclass
class Event:
    timestamp: float


@dataclass
class CollisionEvent(Event):
    collision: Collision

