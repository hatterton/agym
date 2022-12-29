from typing import List, Tuple

import pytest

from agym.games.breakout import ItemManager
from agym.games.breakout.dtos import BreakoutAction, BreakoutActionType
from agym.games.breakout.geom import Point, Rectangle, Vec2

from .dtos import PI, LevelTestCase


@pytest.fixture
def ball_wall_collision_levels(
    ball_vertical_wall_left_collision_level,
    ball_vertical_wall_right_collision_level,
    ball_horisontal_wall_top_collision_level,
    ball_corner_wall_collision_level,
) -> List[LevelTestCase]:
    return [
        ball_vertical_wall_left_collision_level,
        ball_vertical_wall_right_collision_level,
        ball_horisontal_wall_top_collision_level,
        ball_corner_wall_collision_level,
    ]


@pytest.fixture
def ball_vertical_wall_left_collision_level(
    item_manager: ItemManager, env_height
) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball.rect.center = Point(x=60, y=env_height / 2)
    ball.thrown = True
    r2 = 2**0.5
    ball.velocity = Vec2(x=-r2 / 2, y=-r2 / 2)

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
        BreakoutAction(type=BreakoutActionType.NOTHING),
        60,
    )


@pytest.fixture
def ball_vertical_wall_right_collision_level(
    item_manager: ItemManager, env_width, env_height
) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball.rect.center = Point(x=env_width - 60, y=env_height / 2)

    ball.thrown = True
    r2 = 2**0.5
    ball.velocity = Vec2(x=r2 / 2, y=-r2 / 2)

    item_manager.create_wall(
        rect=Rectangle(
            left=env_width,
            top=0,
            width=1.0,
            height=env_height,
        ),
    )

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        60,
    )


@pytest.fixture
def ball_horisontal_wall_top_collision_level(
    item_manager: ItemManager, env_width
) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball.rect.center = Point(x=env_width / 2, y=60)
    ball.thrown = True
    r2 = 2**0.5
    ball.velocity = Vec2(x=r2 / 2, y=-r2 / 2)

    item_manager.create_wall(
        rect=Rectangle(
            left=0.0,
            top=-1,
            width=env_width,
            height=1.0,
        ),
    )

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        60,
    )


@pytest.fixture
def ball_corner_wall_collision_level(
    item_manager: ItemManager, env_width, env_height
) -> LevelTestCase:
    ball = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball.rect.center = Point(x=env_width - 60, y=60)
    ball.thrown = True
    r2 = 2**0.5
    ball.velocity = Vec2(x=r2 / 2, y=-r2 / 2)

    item_manager.create_wall(
        rect=Rectangle(
            left=0.0,
            top=-1.0,
            width=env_width,
            height=1.0,
        ),
    )
    item_manager.create_wall(
        rect=Rectangle(
            left=env_width,
            top=0,
            width=1.0,
            height=env_height,
        ),
    )

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        60,
    )
