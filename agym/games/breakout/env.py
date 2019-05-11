import math
import random

from agym.games import IGameEnviroment
from agym.games.breakout.items import (
    Ball,
    Platform,
    Block,
)
from pygame.sprite import Group


class BreakOutEnv(IGameEnviroment):
    def __init__(self, env_width: int, env_height: int):
        self.env_width = env_width
        self.env_height = env_height
        self.n_actions = 3

        self.ball = Ball(
            image_name="ball_aparture 20x20.png",
            radius=10,
            velocity=10,
        )
        self.platform = Platform(
            image_name="platform 120x20.png",
            velocity=10,
        )
        self.blocks = Group()

    def reset(self):
        self.make_target_wall()

        self.platform.rect.centerx = self.env_width // 2
        self.platform.rect.bottom = self.env_height - 10

        self.ball.move_on_platform(self.platform.rect)
        # image_name = colors[random.randint(0, 2)]

    def make_target_wall(self,
                         n_rows: int = 5,
                         block_width: int = 60,
                         block_height: int = 20,
                         top_shift: int = 50,
                         between_shift: int = 5):
        image_name_template = "block_{} 60x20.png"
        colors = ["blue", "yellow", "red"]

        n_cols = math.floor(
            (self.env_width - between_shift) /
            (block_width + between_shift)
        )
        side_shift = (
            self.env_width -
            n_cols * block_width -
            (n_cols - 1) * between_shift
        ) // 2

        self.blocks.empty()
        for i in range(n_rows):
            for j in range(n_cols):
                image_name = image_name_template.format(
                    colors[random.randint(0, 2)]
                )
                top = (top_shift + i * block_height +
                       (i - 1) * between_shift)
                left = (side_shift + j * block_width +
                        (j - 1) * between_shift)
                block = Block(
                    image_name=image_name,
                    top=top,
                    left=left
                )
                self.blocks.add(block)

    def step(self, action, dt: float):
        return None, None, None

    def get_visual_state(self):
        return None

    def get_flatten_state(self):
        return None

    def blit(self, screen) -> None:
        self.platform.blit(screen)
        self.ball.blit(screen)
        self.blocks.draw(screen)

    def try_event(self, event) -> bool:
        return False
