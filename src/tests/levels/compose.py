from typing import List

import pytest

from envs.breakout import ItemManager

from .ball_ball import *
from .ball_block import *
from .ball_platform import *
from .ball_wall import *
from .dtos import LevelTestCase
from .platform_wall import *


@pytest.fixture
def item_manager():
    return ItemManager()


@pytest.fixture
def all_levels(
    ball_wall_collision_levels,
    platform_wall_collision_levels,
    ball_block_collision_levels,
    ball_platform_collision_levels,
    ball_ball_collision_levels,
) -> List[LevelTestCase]:
    levels = []

    levels += ball_ball_collision_levels
    levels += ball_block_collision_levels
    levels += ball_platform_collision_levels
    levels += ball_wall_collision_levels
    levels += platform_wall_collision_levels

    return levels
