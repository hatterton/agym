import pytest
import math
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
def ball_ball_moving_stop_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball1 = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball1.rect.center = Point(x=100, y=100)
    ball1.thrown = True
    ball1.velocity = Vec2(x=1, y=0)

    ball2 = item_manager.create_ball(
        radius=10,
        speed=0.,
    )
    ball2.rect.center = Point(x=170, y=100)
    ball2.thrown = True
    ball2.velocity = Vec2(x=0, y=0)

    balls = [ball1, ball2]

    platform = item_manager.create_platform(speed=1.)
    platform.rect.center = Point(x=100, y=330)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return (
        Level(blocks=blocks, balls=balls, platform=platform),
        BreakoutAction.NOTHING,
        60,
    )


@pytest.fixture
def ball_ball_angle_stop_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball1 = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball1.rect.center = Point(x=60, y=150)
    ball1.thrown = True
    ball1.velocity = Vec2(x=1/2**0.5, y=-1/2**0.5)

    ball2 = item_manager.create_ball(
        radius=10,
        speed=0.,
    )
    ball2.rect.center = Point(x=100, y=90)
    ball2.thrown = True
    ball2.velocity = Vec2(x=0, y=0)

    balls = [ball1, ball2]

    platform = item_manager.create_platform(speed=1.)
    platform.rect.center = Point(x=100, y=330)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return (
        Level(blocks=blocks, balls=balls, platform=platform),
        BreakoutAction.NOTHING,
        60,
    )


@pytest.fixture
def ball_ball_towards_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball1 = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball1.rect.center = Point(x=50, y=100)
    ball1.thrown = True
    ball1.velocity = Vec2(x=1, y=0)

    ball2 = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball2.rect.center = Point(x=150, y=100)
    ball2.thrown = True
    ball2.velocity = Vec2(x=-1, y=0)

    balls = [ball1, ball2]

    platform = item_manager.create_platform(speed=1.)
    platform.rect.center = Point(x=100, y=330)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return (
        Level(blocks=blocks, balls=balls, platform=platform),
        BreakoutAction.NOTHING,
        50,
    )


@pytest.fixture
def ball_ball_towards_between_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball1 = item_manager.create_ball(
        radius=10,
        speed=1.,
    )
    ball1.rect.center = Point(x=40, y=100)
    ball1.thrown = True
    ball1.velocity = Vec2(x=1, y=0)

    ball2 = item_manager.create_ball(
        radius=10,
        speed=1.,
    )
    ball2.rect.center = Point(x=160, y=100)
    ball2.thrown = True
    ball2.velocity = Vec2(x=-1, y=0)

    ball3 = item_manager.create_ball(
        radius=10,
        speed=1.,
    )
    ball3.rect.center = Point(x=100, y=140)
    ball3.thrown = True
    ball3.velocity = Vec2(x=0, y=-1)

    balls = [ball1, ball2, ball3]

    platform = item_manager.create_platform(speed=1.)
    platform.rect.center = Point(x=100, y=330)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return (
        Level(blocks=blocks, balls=balls, platform=platform),
        BreakoutAction.NOTHING,
        50,
    )



@pytest.fixture
def ball_ball_race_collision_level(item_manager: ItemManager) -> LevelTestCase:
    ball1 = item_manager.create_ball(
        radius=10,
        speed=2.1,
    )
    ball1.rect.center = Point(x=100, y=100)
    ball1.thrown = True
    ball1.velocity = Vec2(x=1, y=0)

    ball2 = item_manager.create_ball(
        radius=10,
        speed=2.,
    )
    ball2.rect.center = Point(x=122, y=100)
    ball2.thrown = True
    ball2.velocity = Vec2(x=1, y=0)

    balls = [ball1, ball2]

    platform = item_manager.create_platform(speed=2.)
    platform.rect.center = Point(x=100, y=330)

    blocks = [
        item_manager.create_block(top=0, left=0)
    ]

    return (
        Level(blocks=blocks, balls=balls, platform=platform),
        BreakoutAction.RIGHT,
        60,
    )


