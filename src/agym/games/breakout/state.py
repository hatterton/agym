from dataclasses import dataclass
from typing import (
    List,
    Iterable,
)

from agym.games.breakout.items import (
    Ball,
    Platform,
    Block,
    Item,
)
from agym.games.breakout.geom import Rectangle


@dataclass
class GameState:
    platforms: List[Platform]
    balls: List[Ball]
    blocks: List[Block]

    wall_rect: Rectangle

    def duplicate_empty(self) -> "GameState":
        return GameState(
            platforms=[],
            balls=[],
            blocks=[],
            wall_rect=self.wall_rect,
        )

    def get_items(self) -> Iterable[Item]:
        yield from self.platforms
        yield from self.balls
        yield from self.blocks
