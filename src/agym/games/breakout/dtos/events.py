from dataclasses import dataclass, field
from typing import Tuple

from agym.dtos import Event
from agym.games.breakout.geom import Point

from .collisions import Collision


@dataclass
class CollisionEvent(Event):
    collision: Collision
