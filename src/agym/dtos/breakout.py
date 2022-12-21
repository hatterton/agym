from enum import Enum, auto


class BreakoutLevelType(Enum):
    DEFAULT = auto()
    PERFORMANCE = auto()


class BreakoutCollisionEngine(Enum):
    NAIVE = auto()
    KDTREE = auto()
