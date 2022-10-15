import pytest
import math
from typing import List, Tuple

from agym.games.breakout import (
    ItemManager,
    Level,
)
from agym.games.breakout.geom import Point, Vec2


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
        speed=2.,
    )
    ball.rect.center = Point(x=100, y=60)
    ball.thrown = True
    ball.velocity = Vec2(x=0, y=1)

    block = item_manager.create_block(top=0, left=0)
    block.rect.center = Point(x=100, y=140)
    blocks = [
        block,
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(speed=0)
    platform.rect.center = Point(x=100, y=330)

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


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
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(speed=0)
    platform.rect.center = Point(x=100, y=330)

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_vertical_wall_left_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball.rect.center = Point(x=60, y=200)
    ball.thrown = True
    r2 = 2 ** 0.5
    ball.velocity = Vec2(x=-r2 / 2, y=-r2 / 2)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(speed=0)
    platform.rect.center = Point(x=100, y=330)

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_vertical_wall_right_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball.rect.center = Point(x=390, y=200)
    ball.thrown = True
    r2 = 2 ** 0.5
    ball.velocity = Vec2(x=r2 / 2, y=-r2 / 2)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(speed=0)
    platform.rect.center = Point(x=100, y=330)

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_vertical_wall_top_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball.rect.center = Point(x=100, y=60)
    ball.thrown = True
    r2 = 2 ** 0.5
    ball.velocity = Vec2(x=r2 / 2, y=-r2 / 2)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(speed=0)
    platform.rect.center = Point(x=100, y=330)

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_corner_wall_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball.rect.center = Point(x=400, y=50)
    ball.thrown = True
    r2 = 2 ** 0.5
    ball.velocity = Vec2(x=r2 / 2, y=-r2 / 2)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(speed=0)
    platform.rect.center = Point(x=100, y=330)

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


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
        item_manager.create_block(top=0, left=0)
    ]

    platform = item_manager.create_platform(speed=0)
    platform.rect.center = Point(x=100, y=330)

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def ball_platform_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball.rect.center = Point(x=300, y=250)
    ball.thrown = True
    ball.velocity = Vec2(x=0, y=1)

    platform = item_manager.create_platform(speed=0)
    platform.rect.center = Point(x=300, y=330)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return Level(blocks=blocks, balls=[ball], platform=platform), 60


@pytest.fixture
def platfrom_left_wall_collision_level(item_manager: ItemManager) -> LevelTestCase:
    platform = item_manager.create_platform(speed=2)
    platform.rect.center = Point(x=150, y=330)
    platform.rect.left = 70
    platform.velocity = Vec2(x=-1, y=0)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return Level(blocks=blocks, balls=[], platform=platform), 60


@pytest.fixture
def platfrom_right_wall_collision_level(item_manager: ItemManager) -> LevelTestCase:
    platform = item_manager.create_platform(speed=2)
    platform.rect.center = Point(x=150, y=330)
    platform.rect.right = 380
    platform.velocity = Vec2(x=1, y=0)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return Level(blocks=blocks, balls=[], platform=platform), 60


@pytest.fixture
def ball_platform_side_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball.rect.center = Point(x=20, y=327)
    ball.thrown = True
    ball.velocity = Vec2(x=1, y=0)

    platform = item_manager.create_platform(speed=1.)
    platform.rect.center = Point(x=100, y=330)
    platform.velocity = Vec2(x=-1, y=0)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

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
    ball_platform_collision_level,
    platfrom_left_wall_collision_level,
    platfrom_right_wall_collision_level,
    ball_platform_side_collision_level,
) -> List[LevelTestCase]:
    return [
        ball_platform_collision_level,
        ball_block_collision_level,
        ball_corner_block_collision_level,
        ball_vertical_wall_left_collision_level,
        ball_vertical_wall_right_collision_level,
        ball_vertical_wall_top_collision_level,
        ball_corner_wall_collision_level,
        ball_between_blocks_collision_level,
        platfrom_left_wall_collision_level,
        platfrom_right_wall_collision_level,
        ball_platform_side_collision_level,
    ]
