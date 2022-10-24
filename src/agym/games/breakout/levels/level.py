from typing import List, Optional
from dataclasses import dataclass

from agym.games.breakout.items import (
    Platform,
    Ball,
    Block,
    Wall,
)


@dataclass
class Level:
    platforms: List[Platform]
    balls: List[Ball]
    blocks: List[Block]
    walls: List[Wall]

