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
def platform_wall_collision_levels(
    platform_left_wall_collision_level,
    platform_right_wall_collision_level,
) -> List[LevelTestCase]:
    return [
        platform_left_wall_collision_level,
        platform_right_wall_collision_level,
    ]


@pytest.fixture
def platform_left_wall_collision_level(item_manager: ItemManager) -> LevelTestCase:
    platform = item_manager.create_platform(speed=2)
    platform.rect.center = Point(x=150, y=330)
    platform.rect.left = 70
    platform.velocity = Vec2(x=-1, y=0)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return (
        Level(blocks=blocks, balls=[], platform=platform),
        BreakoutAction.LEFT,
        60,
    )


@pytest.fixture
def platform_right_wall_collision_level(item_manager: ItemManager) -> LevelTestCase:
    platform = item_manager.create_platform(speed=2)
    platform.rect.center = Point(x=150, y=330)
    platform.rect.right = 380
    platform.velocity = Vec2(x=1, y=0)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return (
        Level(blocks=blocks, balls=[], platform=platform),
        BreakoutAction.RIGHT,
        60,
    )

