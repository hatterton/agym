import math
from typing import List, Tuple

import pytest

from envs.breakout import ItemManager
from envs.breakout import BreakoutAction, BreakoutActionType
from geometry import Point, Vec2

from .dtos import PI, LevelTestCase


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
        speed=2.0,
    )
    ball.rect.center = Point(x=100, y=60)
    ball.thrown = True
    ball.velocity = Vec2(x=0, y=1)

    block = item_manager.create_block(top=0, left=0)
    block.rect.center = Point(x=100, y=140)

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        60,
    )


@pytest.fixture
def ball_corner_block_collision_level(
    item_manager: ItemManager,
) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball.rect.center = Point(x=100 + math.sin(PI / 8) * 10, y=160)
    ball.thrown = True
    ball.velocity = Vec2(x=0, y=-1)

    block = item_manager.create_block(top=100, left=0)
    block.rect.right = 100

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        60,
    )


@pytest.fixture
def ball_between_blocks_collision_level(
    item_manager: ItemManager,
) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball.rect.center = Point(x=100, y=100)
    ball.thrown = True
    ball.velocity = Vec2(x=0, y=1)

    block1 = item_manager.create_block(top=150, left=0)
    block1.rect.right = 95
    block2 = item_manager.create_block(top=150, left=0)
    block2.rect.left = 105

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        60,
    )
