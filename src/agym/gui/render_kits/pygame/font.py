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
        background_color: Optional[Color],
        alpha: Optional[int],
    ) -> PygameScreen:
        fg_color = foreground_color.to_tuple()
        if background_color is None:
            bg_color = None
        else:
            bg_color = background_color.to_tuple()

        pg_screen = self._font.render(text, True, fg_color, bg_color)
        screen = PygameScreen(pg_screen)

        return screen

    def size(self, text: str) -> Size:
        width, height = self._font.size(text)

        return Size(width=width, height=height)
