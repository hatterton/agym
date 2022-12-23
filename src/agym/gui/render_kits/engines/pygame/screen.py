from typing import Optional

import pygame as pg

from agym.dtos import Color, Rect, Shift, Size
from agym.protocols import IScreen


class PygameScreen(IScreen):
    def __init__(self, screen: pg.surface.Surface) -> None:
        self._screen = screen

    @property
    def size(self) -> Size:
        rect = self._screen.get_rect()
        return Size(width=rect.width, height=rect.height)

    @property
    def rect(self) -> Rect:
        return Rect.from_shift_size(shift=Shift(x=0, y=0), size=self.size)

    @property
    def alpha(self) -> int:
        value = self._screen.get_alpha()

        if value is None:
            value = 255

        return value

    @alpha.setter
    def alpha(self, value: int) -> None:
        self._screen.set_alpha(value)

    def fill(self, color: Color, rect: Optional[Rect] = None) -> None:
        if rect is None:
            pygame_rect = None
        else:
            pygame_rect = (rect.shift.to_tuple(), rect.size.to_tuple())

        self._screen.fill(color.to_tuple(), pygame_rect)

    def blit(self, screen: IScreen, shift: Shift) -> None:
        if not isinstance(screen, PygameScreen):
            raise NotImplementedError

        self._screen.blit(screen._screen, shift.to_tuple())

    def resize(self, size: Size) -> "PygameScreen":
        pg_screen = pg.transform.scale(self._screen, size.to_tuple())

        return PygameScreen(pg_screen)
