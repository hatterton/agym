from typing import Optional

import pygame as pg

from agym.dtos import Color, Font, Rect, Screen, Shift


def render_text(
    font: Font,
    text: str,
    foreground_color: Color,
    background_color: Optional[Color] = None,
    alpha: Optional[int] = None,
) -> Screen:
    image_lines = []
    for textline in text.split("\n"):
        image_line = render_line(
            font=font,
            line=textline,
            foreground_color=foreground_color,
            background_color=None,
            alpha=None,
        )
        image_lines.append(image_line)

    width = max([il.get_rect().width for il in image_lines])
    height = sum([il.get_rect().height for il in image_lines])
    image_screen = pg.Surface((width, height)).convert_alpha()

    if background_color is not None:
        fill_screen(image_screen, background_color)
    else:
        fill_screen(image_screen, Color(0, 0, 0, 0))

    shift = Shift(x=0, y=0)
    for image_line in image_lines:
        blit_screen(image_screen, image_line, shift)

        image_height = image_line.get_rect().height
        shift = Shift(
            x=shift.x,
            y=shift.y + image_height,
        )

    if alpha is not None:
        image_screen.set_alpha(alpha)

    return image_screen


def render_line(
    font: Font,
    line: str,
    foreground_color: Color,
    background_color: Optional[Color] = None,
    alpha: Optional[int] = None,
) -> Screen:
    fg_color = foreground_color.to_tuple()
    if background_color is None:
        bg_color = None
    else:
        bg_color = background_color.to_tuple()

    surface = font.render(line, True, fg_color, bg_color)

    if alpha is not None:
        surface.set_alpha(alpha)

    return surface


def blit_screen(parent: Screen, child: Screen, shift: Shift) -> None:
    parent.blit(child, shift.to_tuple())


def fill_screen(
    screen: Screen, color: Color, rect: Optional[Rect] = None
) -> None:
    if rect is None:
        screen.fill(color.to_tuple())
    else:
        screen.fill(color.to_tuple(), rect)
