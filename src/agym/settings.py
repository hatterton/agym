from typing import Tuple

from pydantic import BaseSettings

from agym.dtos import BreakoutCollisionEngine, BreakoutLevelType, Size
from agym.games.breakout.geom import Vec2

Color = Tuple[int, int, int]


class BreakoutSettings(BaseSettings):
    num_envs: int = 3

    image_dir: str = "agym/static/images/breakout"

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

    num_balls: int = 4
    ball_speed: float = 15.0
    ball_radius: float = 15.0


class Settings(BaseSettings):
    window_screen_width: int = 700
    window_screen_height: int = 800

    env_width: int = 600
    env_height: int = 600

    mb_width: int = 150
    mb_height: int = 60
    menu_height: int = 400

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
