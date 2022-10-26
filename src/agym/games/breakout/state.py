from dataclasses import dataclass, field
from typing import (
    List,
    Iterable,
)

from agym.games.breakout.items import (
    Ball,
    Platform,
    Block,
    Wall,
    Item,
)
from agym.games.breakout.geom import Rectangle


@dataclass
class GameState:
    balls: List[Ball] = field(default_factory=list)
    blocks: List[Block] = field(default_factory=list)
    platforms: List[Platform] = field(default_factory=list)
    walls: List[Wall] = field(default_factory=list)

    def duplicate_empty(self) -> "GameState":
        return GameState(
            balls=[],
            blocks=[],
            platforms=[],
            walls=self.walls,
        )

    def get_items(self) -> Iterable[Item]:
        yield from self.balls
        yield from self.blocks
        yield from self.platforms
        yield from self.walls
