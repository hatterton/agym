from dataclasses import dataclass
from enum import Enum

from agym.games.protocols import IGameAction


class BreakoutActionType(Enum):
    NOTHING = 0
    LEFT = 1
    RIGHT = 2
    THROW = 3


@dataclass
class BreakoutAction(IGameAction):
    type: BreakoutActionType
