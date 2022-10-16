import math
from typing import Tuple

from agym.games.breakout import (
    Level,
    BreakoutAction,
)

TickNum = float
LevelTestCase = Tuple[Level, BreakoutAction, TickNum]
PI = math.asin(1) * 2

