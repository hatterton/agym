from enum import Enum, auto


class CollisionType(Enum):
    BALL_WALL = 0
    BALL_PLATFORM = 1
    BALL_BLOCK = 2
    PLATFORM_WALL = 3


class EventType(Enum):
    COLLISION = auto()

