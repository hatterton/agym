import pytest
import math
from typing import List, Tuple

from agym.games.breakout import (
    ItemManager,
    Level,
)


@pytest.fixture
def item_manager():
    return ItemManager()


TickNum = float
LevelTestCase = Tuple[Level, TickNum]
PI = math.asin(1) * 2


@pytest.fixture
def ball_block_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        velocity=2.,
    )
    ball.rect.center = [100, 60]
    ball.thrown = True
    ball.vec_velocity = [0, 1]

    block = item_manager.create_block(top=0, left=0)
    block.rect.center = [100, 140]
    blocks = [
        block,
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(velocity=0)
    platform.rect.center = [100, 480]

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_corner_block_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        velocity=2.,
    )
    ball.rect.center = [100 + math.sin(PI/8) * 10, 160]
    ball.thrown = True
    ball.vec_velocity = [0, -1]

    block = item_manager.create_block(top=100, left=0)
    block.rect.right = 100
    blocks = [
        block,
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(velocity=0)
    platform.rect.center = [100, 480]

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_vertical_wall_left_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        velocity=2.,
    )
    ball.rect.center = [60, 200]
    ball.thrown = True
    r2 = 2 ** 0.5
    ball.vec_velocity = [-r2 / 2, -r2 / 2]

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(velocity=0)
    platform.rect.center = [100, 480]

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_vertical_wall_right_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        velocity=2.,
    )
    ball.rect.center = [390, 200]
    ball.thrown = True
    r2 = 2 ** 0.5
    ball.vec_velocity = [r2 / 2, -r2 / 2]

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(velocity=0)
    platform.rect.center = [100, 480]

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_vertical_wall_top_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        velocity=2.,
    )
    ball.rect.center = [100, 60]
    ball.thrown = True
    r2 = 2 ** 0.5
    ball.vec_velocity = [r2 / 2, -r2 / 2]

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(velocity=0)
    platform.rect.center = [100, 480]

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_corner_wall_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        velocity=2.,
    )
    ball.rect.center = [400, 50]
    ball.thrown = True
    r2 = 2 ** 0.5
    ball.vec_velocity = [r2 / 2, -r2 / 2]

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(velocity=0)
    platform.rect.center = [100, 480]

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_between_blocks_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        velocity=2.,
    )
    ball.rect.center = [100, 100]
    ball.thrown = True
    ball.vec_velocity = [0, 1]

    block1 = item_manager.create_block(top=150, left=0)
    block1.rect.right = 95
    block2 = item_manager.create_block(top=150, left=0)
    block2.rect.left = 105
    blocks = [
        block1,
        block2,
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(velocity=0)
    platform.rect.center = [100, 480]

    return Level(blocks=blocks, balls=[ball], platform=platform), 60



@pytest.fixture
def all_levels(
    ball_block_collision_level,
    ball_corner_block_collision_level,
    ball_vertical_wall_left_collision_level,
    ball_vertical_wall_right_collision_level,
    ball_vertical_wall_top_collision_level,
    ball_corner_wall_collision_level,
    ball_between_blocks_collision_level,
) -> List[LevelTestCase]:
    return [
        ball_block_collision_level,
        ball_corner_block_collision_level,
        ball_vertical_wall_left_collision_level,
        ball_vertical_wall_right_collision_level,
        ball_vertical_wall_top_collision_level,
        ball_corner_wall_collision_level,
        ball_between_blocks_collision_level,
    ]
