from typing import List

import pytest

from envs.breakout import BreakoutAction, BreakoutActionType, ItemManager
from geometry import Point, Vec2

from .dtos import LevelTestCase


@pytest.fixture
def ball_ball_collision_levels(
    ball_ball_moving_stop_collision_level,
    ball_ball_angle_stop_collision_level,
    ball_ball_towards_collision_level,
    ball_ball_towards_between_collision_level,
    ball_ball_race_collision_level,
) -> List[LevelTestCase]:
    return [
        ball_ball_moving_stop_collision_level,
        ball_ball_angle_stop_collision_level,
        ball_ball_towards_collision_level,
        ball_ball_towards_between_collision_level,
        ball_ball_race_collision_level,
    ]


@pytest.fixture
def ball_ball_moving_stop_collision_level(
    item_manager: ItemManager,
) -> LevelTestCase:
    ball1 = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball1.rect.center = Point(x=100, y=100)
    ball1.thrown = True
    ball1.velocity = Vec2(x=1, y=0)

    ball2 = item_manager.create_ball(
        radius=10,
        speed=0.0,
    )
    ball2.rect.center = Point(x=170, y=100)
    ball2.thrown = True
    ball2.velocity = Vec2(x=0, y=0)

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        60,
    )


@pytest.fixture
def ball_ball_angle_stop_collision_level(
    item_manager: ItemManager,
) -> LevelTestCase:
    ball1 = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball1.rect.center = Point(x=60, y=150)
    ball1.thrown = True
    ball1.velocity = Vec2(x=1 / 2**0.5, y=-1 / 2**0.5)

    ball2 = item_manager.create_ball(
        radius=10,
        speed=0.0,
    )
    ball2.rect.center = Point(x=100, y=90)
    ball2.thrown = True
    ball2.velocity = Vec2(x=0, y=0)

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        60,
    )


@pytest.fixture
def ball_ball_towards_collision_level(
    item_manager: ItemManager,
) -> LevelTestCase:
    ball1 = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball1.rect.center = Point(x=50, y=100)
    ball1.thrown = True
    ball1.velocity = Vec2(x=1, y=0)

    ball2 = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball2.rect.center = Point(x=150, y=100)
    ball2.thrown = True
    ball2.velocity = Vec2(x=-1, y=0)

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        50,
    )


@pytest.fixture
def ball_ball_towards_between_collision_level(
    item_manager: ItemManager,
) -> LevelTestCase:
    ball1 = item_manager.create_ball(
        radius=10,
        speed=1.0,
    )
    ball1.rect.center = Point(x=40, y=100)
    ball1.thrown = True
    ball1.velocity = Vec2(x=1, y=0)

    ball2 = item_manager.create_ball(
        radius=10,
        speed=1.0,
    )
    ball2.rect.center = Point(x=160, y=100)
    ball2.thrown = True
    ball2.velocity = Vec2(x=-1, y=0)

    ball3 = item_manager.create_ball(
        radius=10,
        speed=1.0,
    )
    ball3.rect.center = Point(x=100, y=140)
    ball3.thrown = True
    ball3.velocity = Vec2(x=0, y=-1)

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.NOTHING),
        50,
    )


@pytest.fixture
def ball_ball_race_collision_level(
    item_manager: ItemManager, env_height: float
) -> LevelTestCase:
    ball1 = item_manager.create_ball(
        radius=10,
        speed=2.1,
    )
    ball1.rect.center = Point(x=100, y=100)
    ball1.thrown = True
    ball1.velocity = Vec2(x=1, y=0)

    ball2 = item_manager.create_ball(
        radius=10,
        speed=2.0,
    )
    ball2.rect.center = Point(x=122, y=100)
    ball2.thrown = True
    ball2.velocity = Vec2(x=1, y=0)

    platform = item_manager.create_platform(speed=2.0)
    platform.rect.left = 1
    platform.rect.bottom = env_height

    return (
        item_manager.extract_state(),
        BreakoutAction(type=BreakoutActionType.RIGHT),
        60,
    )
