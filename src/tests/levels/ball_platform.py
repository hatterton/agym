from typing import List

import pytest

from envs.breakout import BreakoutAction, BreakoutActionType, ItemManager
from geometry import Rectangle, Vec2

from .dtos import LevelTestCase


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
def ball_platform_collision_level(
    item_manager: ItemManager, env_width: float, env_height: float
) -> LevelTestCase:
    platform = item_manager.create_platform(speed=0)
    platform.rect.centerx = env_width / 2
    platform.rect.bottom = env_height

    ball = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball.rect.centerx = platform.rect.centerx
    ball.rect.bottom = platform.rect.top - 50
    ball.thrown = True
    ball.velocity = Vec2(x=0, y=1)

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        60,
    )


@pytest.fixture
def ball_platform_side_collision_level(
    item_manager: ItemManager, env_width: float, env_height: float
) -> LevelTestCase:
    platform = item_manager.create_platform(speed=1.0)
    platform.rect.left = 35
    platform.rect.bottom = env_height

    ball = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball.rect.centery = platform.rect.centery
    ball.rect.left = 1
    ball.thrown = True
    ball.velocity = Vec2(x=1, y=0)

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
        BreakoutAction(type=BreakoutActionType.LEFT),
        40,
    )


@pytest.fixture
def ball_platform_race_collision_level(
    item_manager: ItemManager, env_width: float, env_height: float
) -> LevelTestCase:
    platform = item_manager.create_platform(speed=2.0)
    platform.rect.left = 50
    platform.rect.bottom = env_height

    ball = item_manager.create_ball(
        radius=10,
        speed=2.1,
    )
    ball.rect.centery = platform.rect.centery
    ball.rect.right = platform.rect.left - 2
    ball.thrown = True
    ball.velocity = Vec2(x=1, y=0)

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.RIGHT),
        60,
    )
