from typing import List, Tuple

import pytest

from agym.games.breakout import BreakoutAction, ItemManager
from agym.games.breakout.geom import Point, Rectangle, Vec2

from .dtos import PI, LevelTestCase


@pytest.fixture
def ball_platform_collision_levels(
    ball_platform_collision_level,
    ball_platform_side_collision_level,
    ball_platform_race_collision_level,
) -> List[LevelTestCase]:
    return [
        ball_platform_collision_level,
        ball_platform_side_collision_level,
        ball_platform_race_collision_level,
    ]


@pytest.fixture
def ball_platform_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball.rect.center = Point(x=300, y=250)
    ball.thrown = True
    ball.velocity = Vec2(x=0, y=1)

    platform = item_manager.create_platform(speed=0)
    platform.rect.center = Point(x=300, y=330)

    return (
        item_manager.extract_state(),
        BreakoutAction.NOTHING,
        60,
    )


@pytest.fixture
def ball_platform_side_collision_level(
    item_manager: ItemManager, env_height
) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball.rect.center = Point(x=11, y=327)
    ball.thrown = True
    ball.velocity = Vec2(x=1, y=0)

    platform = item_manager.create_platform(speed=1.0)
    platform.rect.center = Point(x=90, y=330)
    platform.velocity = Vec2(x=-1, y=0)

    item_manager.create_wall(
        rect=Rectangle(
            left=-1.0,
            top=0,
            width=1.0,
            height=env_height,
        ),
    )

    return (
        item_manager.extract_state(),
        BreakoutAction.LEFT,
        40,
    )


@pytest.fixture
def ball_platform_race_collision_level(
    item_manager: ItemManager,
) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.1,
    )
    ball.rect.center = Point(x=27, y=327)
    ball.thrown = True
    ball.velocity = Vec2(x=1, y=0)

    platform = item_manager.create_platform(speed=2.0)
    platform.rect.center = Point(x=100, y=330)

    return (
        item_manager.extract_state(),
        BreakoutAction.RIGHT,
        60,
    )
