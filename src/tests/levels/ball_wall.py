import pytest
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
def ball_wall_collision_levels(
    ball_vertical_wall_left_collision_level,
    ball_vertical_wall_right_collision_level,
    ball_vertical_wall_top_collision_level,
    ball_corner_wall_collision_level,
) -> List[LevelTestCase]:
    return [
        ball_vertical_wall_left_collision_level,
        ball_vertical_wall_right_collision_level,
        ball_vertical_wall_top_collision_level,
        ball_corner_wall_collision_level,
    ]


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

    return (
        Level(blocks=blocks, balls=[ball], platform=platform),
        BreakoutAction.NOTHING,
        60,
    )


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

    return (
        Level(blocks=blocks, balls=[ball], platform=platform),
        BreakoutAction.NOTHING,
        60,
    )


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

    return (
        Level(blocks=blocks, balls=[ball], platform=platform),
        BreakoutAction.NOTHING,
        60,
    )



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

    return (
        Level(blocks=blocks, balls=[ball], platform=platform),
        BreakoutAction.NOTHING,
        60,
    )

