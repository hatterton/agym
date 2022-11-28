from typing import Optional, Tuple

import pygame as pg

from agym.dtos import Color, Shift
from agym.rendering import blit_screen, render_text


class TextLabel:
    def __init__(
        self,
        shift: Shift,
        # font_path: str,
        font_size: int = 20,
        foreground_color: Color = Color(30, 30, 30),
        background_color: Optional[Color] = None,
        alpha: Optional[int] = None,
        text: str = "",
    ):
        self._shift = shift

        self._foreground_color = foreground_color
        self._background_color = background_color
        self._alpha = alpha

        # self._font = pg.font.Font(font_path, font_size)
        self._font = pg.font.SysFont("Hack", font_size)

        self.text = text

    def blit(self, screen: pg.surface.Surface) -> None:
        text_screen = render_text(
            font=self._font,
            text=self.text,
            foreground_color=self._foreground_color,
            background_color=self._background_color,
            alpha=self._alpha,
        )

        blit_screen(screen, text_screen, self._shift)
