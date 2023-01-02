from copy import deepcopy
from dataclasses import dataclass, field
from typing import Iterable, List

from agym.games.breakout.dtos import Ball, Block, Item, Platform, Wall
from agym.games.breakout.geom import Rectangle


@dataclass
class BreakoutState:
    balls: List[Ball] = field(default_factory=list)
    blocks: List[Block] = field(default_factory=list)
    platforms: List[Platform] = field(default_factory=list)
    walls: List[Wall] = field(default_factory=list)

    def get_items(self) -> Iterable[Item]:
        yield from self.balls
        yield from self.blocks
        yield from self.platforms
        yield from self.walls

    def copy(self) -> "BreakoutState":
        balls = [deepcopy(ball) for ball in self.balls]
        blocks = [deepcopy(block) for block in self.blocks]
        platforms = [deepcopy(platform) for platform in self.platforms]
        walls = [deepcopy(wall) for wall in self.walls]

        return BreakoutState(
            balls=balls,
            blocks=blocks,
            platforms=platforms,
            walls=walls,
        )
