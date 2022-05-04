from typing import Tuple

from pydantic import BaseSettings


Color = Tuple[int, int, int]

class Settings(BaseSettings):
    window_screen_width: int = 600
    window_screen_height: int = 600

    env_width: int = 450
    env_height: int = 500

    mb_width: int = 150
    mb_height: int = 60
    menu_height: int = 400

    cirle_color: Color = (200, 50, 50)
    bg_color: Color = (130, 130, 130)
    ga_bg_color: Color = (130, 160, 230)

    max_lives: int = 1
    default_reward: int = 10
    catch_reward: int = 250

    # max_fps: int = 60
    max_fps: int = 500

