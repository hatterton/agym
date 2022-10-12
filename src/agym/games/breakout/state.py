from dataclasses import dataclass
from typing import List

from .items import (
    Ball,
    Platform,
    Block,
)
from .geom import Rectangle


@dataclass
class GameState:
    platforms: List[Platform]
    balls: List[Ball]
    blocks: List[Block]

    wall_rect: Rectangle