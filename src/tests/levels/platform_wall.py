from typing import List, Tuple

import pytest

from agym.games.breakout import ItemManager
from agym.games.breakout.dtos import BreakoutAction, BreakoutActionType
from agym.games.breakout.geom import Point, Rectangle, Vec2

from .dtos import PI, LevelTestCase


@pytest.fixture
def platform_wall_collision_levels(
    platform_left_wall_collision_level,
    platform_right_wall_collision_level,
) -> List[LevelTestCase]:
    return [
        platform_left_wall_collision_level,
        platform_right_wall_collision_level,
    ]


@pytest.fixture
def platform_left_wall_collision_level(
    item_manager: ItemManager, env_height
) -> LevelTestCase:
    platform = item_manager.create_platform(speed=5)
    platform.rect.bottom = env_height
    platform.rect.left = 60
    platform.velocity = Vec2(x=-1, y=0)

    item_manager.create_wall(
        rect=Rectangle(
            left=-1.0,
            top=0.0,
            width=1.0,
            height=env_height,
        ),
    )

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.LEFT),
        60,
    )


@pytest.fixture
def platform_right_wall_collision_level(
    item_manager: ItemManager, env_width, env_height
) -> LevelTestCase:
    platform = item_manager.create_platform(speed=5)
    platform.rect.bottom = env_height
    platform.rect.right = env_width - 60
    platform.velocity = Vec2(x=1, y=0)

    item_manager.create_wall(
        rect=Rectangle(
            left=env_width,
            top=0.0,
            width=1.0,
            height=env_height,
        ),
    )

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.RIGHT),
        60,
    )
