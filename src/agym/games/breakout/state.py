from copy import copy
from dataclasses import dataclass, field
from typing import Iterable, List

from agym.games.breakout.dtos import Ball, Block, Item, Platform, Wall
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

    def copy(self) -> "GameState":
        balls = [copy(ball) for ball in self.balls]
        blocks = [copy(block) for block in self.blocks]
        platforms = [copy(platform) for platform in self.platforms]
        walls = [copy(wall) for wall in self.walls]

        for old_p, new_p in zip(self.platforms, platforms):
            new_p.rect = old_p.rect.copy()
            new_p.velocity = old_p.velocity.copy()

        for old_b, new_b in zip(self.balls, balls):
            new_b.rect = old_b.rect.copy()
            new_b.velocity = old_b.velocity.copy()

        return GameState(
            balls=balls,
            blocks=blocks,
            platforms=platforms,
            walls=walls,
        )
