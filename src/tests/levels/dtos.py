import math
from typing import Tuple

from envs.breakout import BreakoutAction, BreakoutState

TickNum = float
LevelTestCase = Tuple[BreakoutState, BreakoutAction, TickNum]
PI = math.asin(1) * 2
