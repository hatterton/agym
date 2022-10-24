import pytest
import math
from typing import List, Tuple

from agym.games.breakout import (
    ItemManager,
    BreakoutAction,
    Level,
)
from agym.games.breakout.geom import Point, Vec2
from .dtos import (
    LevelTestCase,
    PI,
)


@pytest.fixture
def ball_block_collision_levels(
    ball_block_collision_level,
    ball_corner_block_collision_level,
    ball_between_blocks_collision_level,
) -> List[LevelTestCase]:
    return [
        ball_block_collision_level,
        ball_corner_block_collision_level,
        ball_between_blocks_collision_level,
    ]


@pytest.fixture
def ball_block_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball.rect.center = Point(x=100, y=60)
    ball.thrown = True
    ball.velocity = Vec2(x=0, y=1)

    block = item_manager.create_block(top=0, left=0)
    block.rect.center = Point(x=100, y=140)
    blocks = [
        block,
    ]

    platforms = []

    return (
        Level(blocks=blocks, balls=[ball], platforms=platforms, walls=[]),
        BreakoutAction.NOTHING,
        60,
    )


@pytest.fixture
def ball_corner_block_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball.rect.center = Point(x=100 + math.sin(PI/8) * 10, y=160)
    ball.thrown = True
    ball.velocity = Vec2(x=0, y=-1)

    block = item_manager.create_block(top=100, left=0)
    block.rect.right = 100
    blocks = [
        block,
    ]

    platforms = []

    return (
        Level(blocks=blocks, balls=[ball], platforms=platforms, walls=[]),
        BreakoutAction.NOTHING,
        60,
    )


@pytest.fixture
def ball_between_blocks_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball.rect.center = Point(x=100, y=100)
    ball.thrown = True
    ball.velocity = Vec2(x=0, y=1)

    block1 = item_manager.create_block(top=150, left=0)
    block1.rect.right = 95
    block2 = item_manager.create_block(top=150, left=0)
    block2.rect.left = 105
    blocks = [
        block1,
        block2,
    ]

    platforms = []
    # platform = item_manager.create_platform(speed=0)
    # platform.rect.center = Point(x=100, y=330)

    return (
        Level(blocks=blocks, balls=[ball], platforms=platforms, walls=[]),
        BreakoutAction.NOTHING,
        60,
    )
