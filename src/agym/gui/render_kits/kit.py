from typing import Optional

from agym.dtos import Color, Rect, Shift, Size
from agym.protocols import IFont, IRenderKit, IRenderKitEngine, IScreen


class RenderKit(IRenderKit):
    def __init__(self, engine: IRenderKitEngine) -> None:
        self._engine = engine

    def create_display(
        self,
        size: Size,
    ) -> IScreen:
        return self._engine.create_display(size)

    def flip_display(
        self,
    ) -> None:
        return self._engine.flip_display()

    def create_screen(
        self,
        size: Size,
        background_color: Optional[Color] = None,
    ) -> IScreen:
        return self._engine.create_screen(
            size=size,
            background_color=background_color,
        )

    def create_font(
        self,
        name: str,
        size: int,
    ) -> IFont:
        return self._engine.create_font(name, size)

    def load_font(
        self,
        path: str,
        size: int,
    ) -> IFont:
        return self._engine.load_font(path, size)

    def load_image(
        self,
        path: str,
    ) -> IScreen:
        return self._engine.load_image(path)

    def render_text(
        self,
        text: str,
        font: IFont,
        foreground_color: Color,
        background_color: Optional[Color] = None,
        alpha: Optional[int] = None,
    ) -> IScreen:
        textline_screens = []
        for textline in text.split("\n"):
            textline_screen = font.render(
                text=textline,
                foreground_color=foreground_color,
                background_color=None,
                alpha=None,
            )
            textline_screens.append(textline_screen)

        width = max([il.size.width for il in textline_screens])
        height = sum([il.size.height for il in textline_screens])
        text_screen = self._engine.create_screen(Size(width, height))

        if background_color is not None:
            text_screen.fill(background_color)

        shift = Shift(x=0, y=0)
        for textline_screen in textline_screens:
            text_screen.blit(textline_screen, shift)

            image_height = textline_screen.size.height
            shift = Shift(
                x=shift.x,
                y=shift.y + image_height,
            )

        if alpha is not None:
            text_screen.alpha = alpha

        return text_screen

    def draw_rect(
        self,
        screen: IScreen,
        rect: Rect,
        color: Color,
        width: int = 0,
    ) -> None:
        self._engine.draw_rect(
            screen=screen,
            rect=rect,
            color=color,
            width=width,
        )
