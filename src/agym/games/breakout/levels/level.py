from typing import List, Optional
from dataclasses import dataclass

from ..items import Platform, Ball, Block

@dataclass
class Level:
    platform: Platform
    balls: List[Ball]
    blocks: List[Block]

