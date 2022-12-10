from typing import Optional

import pygame as pg

from agym.dtos import Color, Rect, Shift, Size
from agym.protocols import IRenderKitEngine, IScreen

from .font import PygameFont
from .screen import PygameScreen


class PygameRenderKitEngine(IRenderKitEngine):
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
        else:
            screen.fill(Color(0, 0, 0, 0))

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

    def draw_rect(
        self,
        screen: IScreen,
        rect: Rect,
        color: Color,
        width: int = 0,
    ) -> None:
        if not isinstance(screen, PygameScreen):
            raise NotImplementedError

        pg.draw.rect(
            screen._screen,
            color.to_tuple(),
            (rect.shift.to_tuple(), rect.size.to_tuple()),
            width,
        )

    def draw_line(
        self,
        screen: IScreen,
        start: Shift,
        finish: Shift,
        color: Color,
        width: int = 1,
    ) -> None:
        if not isinstance(screen, PygameScreen):
            raise NotImplementedError

        pg.draw.line(
            screen._screen,
            color.to_tuple(),
            start.to_tuple(),
            finish.to_tuple(),
            width,
        )

    def draw_circle(
        self,
        screen: IScreen,
        center: Shift,
        radius: int,
        color: Color,
        width: int = 0,
    ) -> None:
        if not isinstance(screen, PygameScreen):
            raise NotImplementedError

        pg.draw.circle(
            screen._screen,
            color.to_tuple(),
            center.to_tuple(),
            radius,
            width,
        )
