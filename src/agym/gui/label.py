from typing import Optional

from agym.dtos import Color
from agym.protocols import IFont, IRenderer, IRenderKit, IScreen


class TextLabel(IRenderer):
    def __init__(
        self,
        render_kit: IRenderKit,
        font: IFont,
        foreground_color: Color = Color(30, 30, 30),
        background_color: Optional[Color] = None,
        alpha: Optional[int] = None,
        text: str = "",
    ):
        self._render_kit = render_kit

        self._font = font
        self._foreground_color = foreground_color
        self._background_color = background_color
        self._alpha = alpha

        self._text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    def render(self) -> IScreen:
        screen = self._render_kit.render_text(
            text=self.text,
            font=self._font,
            foreground_color=self._foreground_color,
            background_color=self._background_color,
            alpha=self._alpha,
        )

        return screen
