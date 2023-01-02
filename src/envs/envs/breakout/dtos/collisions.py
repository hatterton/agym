from dataclasses import dataclass
from typing import Iterable

from geometry import Point

from .items import Ball, Block, ItemId, Platform, Wall


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
