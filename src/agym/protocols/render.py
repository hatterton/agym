from typing import Optional, Protocol

from agym.dtos import Color, Rect, Shift, Size


class IScreen(Protocol):
    @property
    def size(self) -> Size:
        pass

    @property
    def rect(self) -> Rect:
        pass

    @property
    def alpha(self) -> int:
        pass

    @alpha.setter
    def alpha(self, value: int) -> None:
        pass

    def fill(self, color: Color, rect: Optional[Rect] = None) -> None:
        pass

    def blit(self, screen: "IScreen", shift: Shift) -> None:
        pass


class IFont(Protocol):
    def render(
        self,
        text: str,
        foreground_color: Color,
        background_color: Optional[Color] = None,
        alpha: Optional[int] = None,
    ) -> IScreen:
        pass

    def size(self, text: str) -> Size:
        pass


class IRenderKitEngine(Protocol):
    def create_display(
        self,
        size: Size,
    ) -> IScreen:
        pass

    def flip_display(
        self,
    ) -> None:
        pass

    def create_screen(
        self,
        size: Size,
        background_color: Optional[Color] = None,
    ) -> IScreen:
        pass

    def create_font(
        self,
        name: str,
        size: int,
    ) -> IFont:
        pass

    def load_font(
        self,
        path: str,
        size: int,
    ) -> IFont:
        pass

    def load_image(
        self,
        path: str,
    ) -> IScreen:
        pass

    def draw_rect(
        self,
        screen: IScreen,
        rect: Rect,
        color: Color,
        width: int = 0,
    ) -> None:
        pass

    def draw_line(
        self,
        screen: IScreen,
        start: Shift,
        finish: Shift,
        color: Color,
        width: int = 1,
    ) -> None:
        pass

    def draw_circle(
        self,
        screen: IScreen,
        center: Shift,
        radius: int,
        color: Color,
        width: int = 0,
    ) -> None:
        pass


class IRenderKit(IRenderKitEngine, Protocol):
    def render_text(
        self,
        text: str,
        font: IFont,
        foreground_color: Color,
        background_color: Optional[Color] = None,
        alpha: Optional[int] = None,
    ) -> IScreen:
        pass


class IRenderer(Protocol):
    def render(self) -> IScreen:
        pass
