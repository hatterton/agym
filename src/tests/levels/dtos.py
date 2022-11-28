import math
from typing import Tuple

from agym.games.breakout import BreakoutAction, GameState

TickNum = float
LevelTestCase = Tuple[GameState, BreakoutAction, TickNum]
PI = math.asin(1) * 2
