from typing import Tuple

from pydantic import BaseSettings

from agym.dtos import (
    BreakoutCollisionEngine,
    BreakoutLevelType,
    EnvironmentType,
    IOFrameworkType,
    Size,
)
from geometry import Vec2

Color = Tuple[int, int, int]


class BreakoutSettings(BaseSettings):
    env_size: Vec2 = Vec2(x=400, y=400)
    num_envs: int = 3

    image_dir: str = "../static/envs/breakout/images"

    # level_type: BreakoutLevelType = BreakoutLevelType.DEFAULT
    level_type: BreakoutLevelType = BreakoutLevelType.PERFORMANCE

    # collision_engine: BreakoutCollisionEngine = BreakoutCollisionEngine.NAIVE
    collision_engine: BreakoutCollisionEngine = BreakoutCollisionEngine.KDTREE

    game_speed: float = 1

    block_wall_num_rows: int = 3
    block_size: Vec2 = Vec2(x=90, y=30)
    block_wall_top_shift: float = 60
    block_wall_between_shift: float = 30

    platform_speed: float = 10
    platform_size: Vec2 = Vec2(x=200, y=25)

    num_balls: int = 5
    ball_speed: float = 15.0
    ball_radius: float = 15.0


class Settings(BaseSettings):
    window_screen_size: Size = Size(width=700, height=800)
    env_screen_size: Size = Size(width=600, height=600)
    subenv_screen_size: Size = Size(width=200, height=200)

    io_framework_type: IOFrameworkType = IOFrameworkType.PYGAME
    environment_type: EnvironmentType = EnvironmentType.BREAKOUT

    cirle_color: Color = (200, 50, 50)
    bg_color: Color = (130, 130, 130)
    ga_bg_color: Color = (130, 160, 230)

    breakout = BreakoutSettings()

    # rendering_kdtree: bool = True
    rendering_kdtree: bool = False

    tps: int = 20

    log_framerate: float = 2.0

    graphics_framerate: float = 1000
    framerate_history_size: int = 400
