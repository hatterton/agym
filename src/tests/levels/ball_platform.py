import pytest
from typing import List, Tuple

from agym.games.breakout import (
    ItemManager,
    BreakoutAction,
    Level,
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

    return (
        Level(blocks=blocks, balls=[ball], platforms=[platform], walls=[]),
        BreakoutAction.NOTHING,
        60,
    )


@pytest.fixture
def ball_platform_side_collision_level(item_manager: ItemManager, env_height) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball.rect.center = Point(x=20, y=327)
    ball.thrown = True
    ball.velocity = Vec2(x=1, y=0)

    platform = item_manager.create_platform(speed=1.)
    platform.rect.center = Point(x=140, y=330)
    platform.velocity = Vec2(x=-1, y=0)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    walls = [
        item_manager.create_wall(
            rect=Rectangle(
                left=-1.,
                top=0,
                width=1.,
                height=env_height,
            ),
        ),
    ]

    return (
        Level(blocks=blocks, balls=[ball], platforms=[platform], walls=walls),
        BreakoutAction.LEFT,
        80,
    )


@pytest.fixture
def ball_platform_race_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.1,
    )
    ball.rect.center = Point(x=27, y=327)
    ball.thrown = True
    ball.velocity = Vec2(x=1, y=0)

    platform = item_manager.create_platform(speed=2.)
    platform.rect.center = Point(x=100, y=330)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return (
        Level(blocks=blocks, balls=[ball], platforms=[platform], walls=[]),
        BreakoutAction.RIGHT,
        60,
    )
