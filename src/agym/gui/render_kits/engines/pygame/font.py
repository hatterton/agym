from typing import Optional

import pygame as pg

from agym.dtos import Color, Rect, Shift, Size
from agym.protocols import IFont

from .screen import PygameScreen


class PygameFont(IFont):
    def __init__(self, font: pg.font.Font) -> None:
        self._font = font

    def render(
        self,
        text: str,
        foreground_color: Color,
        background_color: Optional[Color] = None,
        alpha: Optional[int] = None,
    ) -> PygameScreen:
        fg_color = foreground_color.to_tuple()

        pg_text_screen = self._font.render(text, True, fg_color)
        text_screen = PygameScreen(pg_text_screen)
        text_screen.alpha = foreground_color.alpha

        pg_screen = pg.surface.Surface(
            text_screen.size.to_tuple()
        ).convert_alpha()
        screen = PygameScreen(pg_screen)

        if background_color is not None:
            screen.fill(background_color)
        else:
            screen.fill(Color(0, 0, 0, 0))

        screen.blit(text_screen, Shift(0, 0))

        return screen

    def size(self, text: str) -> Size:
        width, height = self._font.size(text)

        return Size(width=width, height=height)
