from itertools import combinations, product
from typing import Iterable, List

from envs.breakout.dtos import (
    Ball,
    Block,
    Collision,
    CollisionBallBall,
    CollisionBallBlock,
    CollisionBallPlatform,
    CollisionBallWall,
    CollisionPlatformWall,
    Platform,
    Wall,
)
from envs.breakout.state import BreakoutState

from .cached_collection import CachedCollection
from .legacy_collision import (
    calculate_ball_block_colls,
    calculate_ball_platform_colls,
    calculate_ball_wall_colls,
    calculate_platform_wall_colls,
)
from .precise import calculate_ball_ball_colls


class NaiveCollisionDetectionEngine:
    def generate_step_collisions(
        self, state: BreakoutState, dt: float
    ) -> Iterable[Collision]:
        return CachedCollection(
            self.calculate_colls(
                walls=state.walls,
                platforms=state.platforms,
                balls=state.balls,
                blocks=state.blocks,
                dt=dt,
            )
        )

    def calculate_colls(
        self,
        walls: List[Wall],
        platforms: List[Platform],
        balls: List[Ball],
        blocks: List[Block],
        dt: float,
    ) -> Iterable[Collision]:
        yield from self.calculate_balls_balls_colls(balls, dt)
        yield from self.calculate_platforms_walls_colls(platforms, walls, dt)
        yield from self.calculate_balls_walls_colls(balls, walls, dt)
        yield from self.calculate_balls_platforms_colls(balls, platforms, dt)
        yield from self.calculate_balls_blocks_colls(balls, blocks, dt)

    def calculate_balls_balls_colls(
        self, balls: List[Ball], dt: float
    ) -> Iterable[CollisionBallBall]:
        for ball1, ball2 in combinations(balls, 2):
            coll = calculate_ball_ball_colls(ball1, ball2, dt)

            if coll is not None:
                yield coll

    def calculate_balls_blocks_colls(
        self, balls: List[Ball], blocks: List[Block], dt: float
    ) -> Iterable[CollisionBallBlock]:
        for ball, block in product(balls, blocks):
            yield from calculate_ball_block_colls(ball, block, dt)

    def calculate_balls_platforms_colls(
        self, balls: List[Ball], platforms: List[Platform], dt: float
    ) -> Iterable[CollisionBallPlatform]:
        for ball, platform in product(balls, platforms):
            yield from calculate_ball_platform_colls(ball, platform, dt)

    def calculate_balls_walls_colls(
        self, balls: List[Ball], walls: List[Wall], dt: float
    ) -> Iterable[CollisionBallWall]:
        for ball, wall in product(balls, walls):
            yield from calculate_ball_wall_colls(ball, wall, dt)

    def calculate_platforms_walls_colls(
        self, platforms: List[Platform], walls: List[Wall], dt: float
    ) -> Iterable[CollisionPlatformWall]:
        for platform, wall in product(platforms, walls):
            yield from calculate_platform_wall_colls(platform, wall, dt)
