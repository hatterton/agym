from typing import (
    Iterable,
)
from dataclasses import dataclass

from agym.games.breakout.geom import Point
from agym.games.breakout.items import (
    ItemId,
    Ball,
    Block,
    Platform,
    Wall,
)


@dataclass
class Collision:
    point: Point

    @property
    def item_ids(self) -> Iterable[ItemId]:
        return []


@dataclass
class CollisionBallBlock(Collision):
    ball: Ball
    block: Block

    @property
    def item_ids(self) -> Iterable[ItemId]:
        return [self.ball.id, self.block.id]


@dataclass
class CollisionBallPlatform(Collision):
    ball: Ball
    platform: Platform

    @property
    def item_ids(self) -> Iterable[ItemId]:
        return [self.ball.id, self.platform.id]


@dataclass
class CollisionBallWall(Collision):
    ball: Ball
    wall: Wall

    @property
    def item_ids(self) -> Iterable[ItemId]:
        return [self.ball.id, self.wall.id]


@dataclass
class CollisionPlatformWall(Collision):
    platform: Platform
    wall: Wall

    @property
    def item_ids(self) -> Iterable[ItemId]:
        return [self.platform.id, self.wall.id]


@dataclass
class CollisionBallBall(Collision):
    ball1: Ball
    ball2: Ball

    @property
    def item_ids(self) -> Iterable[ItemId]:
        return [self.ball1.id, self.ball2.id]
