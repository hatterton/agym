import pytest
from typing import List, Tuple

from agym.games.breakout import (
    ItemManager,
    BreakoutAction,
)
from agym.games.breakout.geom import (
    Point,
    Vec2,
    Rectangle,
)
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
def platform_left_wall_collision_level(item_manager: ItemManager, env_height) -> LevelTestCase:
    platform = item_manager.create_platform(speed=5)
    platform.rect.center = Point(x=150, y=330)
    platform.rect.left = 70
    platform.velocity = Vec2(x=-1, y=0)

    item_manager.create_wall(
        rect=Rectangle(
            left=-1.,
            top=0.,
            width=1.,
            height=env_height,
        ),
    )

    return (
        item_manager.extract_state(),
        BreakoutAction.LEFT,
        60,
    )


@pytest.fixture
def platform_right_wall_collision_level(item_manager: ItemManager, env_width, env_height) -> LevelTestCase:
    platform = item_manager.create_platform(speed=5)
    platform.rect.center = Point(x=150, y=330)
    platform.rect.right = 380
    platform.velocity = Vec2(x=1, y=0)

    item_manager.create_wall(
        rect=Rectangle(
            left=env_width,
            top=0.,
            width=1.,
            height=env_height,
        ),
    )

    return (
        item_manager.extract_state(),
        BreakoutAction.RIGHT,
        60,
    )

