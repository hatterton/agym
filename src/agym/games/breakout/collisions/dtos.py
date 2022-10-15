from dataclasses import dataclass
from ..geom import Point
from ..items import (
    Ball,
    Block,
    Platform,
)


@dataclass
class Collision:
    point: Point


@dataclass
class CollisionBallBlock(Collision):
    ball: Ball
    block: Block


@dataclass
class CollisionBallPlatform(Collision):
    ball: Ball
    platform: Platform


@dataclass
class CollisionBallWall(Collision):
    ball: Ball


@dataclass
class CollisionPlatformWall(Collision):
    platform: Platform


@dataclass
class CollisionBallBall(Collision):
    ball1: Ball
    ball2: Ball
