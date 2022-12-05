from typing import Optional

import pygame as pg

from agym.dtos import Color, Shift, Size
from agym.protocols import IRenderKit

from .font import PygameFont
from .screen import PygameScreen


class PygameRenderKit(IRenderKit):
    def create_display(
        self,
        size: Size,
    ) -> PygameScreen:
        pg_screen = pg.display.set_mode((size.width, size.height))
        screen = PygameScreen(pg_screen)

        return screen

    def flip_display(
        self,
    ) -> None:
        pg.display.flip()

    def create_screen(
        self,
        size: Size,
        background_color: Optional[Color] = None,
    ) -> PygameScreen:
        pg_screen = pg.Surface((size.width, size.height)).convert_alpha()
        screen = PygameScreen(pg_screen)

        if background_color is not None:
            screen.fill(background_color)

        return screen

    def create_font(
        self,
        name: str,
        size: int,
    ) -> PygameFont:
        pg_font = pg.font.SysFont(name, size)
        font = PygameFont(pg_font)

        return font

    def load_font(
        self,
        path: str,
        size: int,
    ) -> PygameFont:
        pg_font = pg.font.Font(path, size)
        font = PygameFont(pg_font)

        return font

    def load_image(
        self,
        path: str,
    ) -> PygameScreen:
        image = pg.image.load(path)
        screen = PygameScreen(image)

        return screen
