from dataclasses import dataclass, field
from typing import Tuple

from .dtos import EventType, CollisionType
from .geom import Point


@dataclass
class Event:
    type: EventType
    timestamp: float


@dataclass
class CollisionEvent(Event):
    type: EventType = field(default=EventType.COLLISION, init=False)
    collision_type: CollisionType
    point: Point

