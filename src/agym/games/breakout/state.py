from dataclasses import dataclass
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
    platforms: List[Platform]
    balls: List[Ball]
    blocks: List[Block]
    walls: List[Wall]

    def duplicate_empty(self) -> "GameState":
        return GameState(
            platforms=[],
            balls=[],
            blocks=[],
            walls=self.walls,
        )

    def get_items(self) -> Iterable[Item]:
        yield from self.walls
        yield from self.platforms
        yield from self.balls
        yield from self.blocks
