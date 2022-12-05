from typing import Any, List, Optional, Protocol, Tuple

from .dtos import (
    Color,
    Event,
    PygameEvent,
    PygameFont,
    PygameRect,
    PygameScreen,
    Rect,
    Shift,
    Size,
)


class IUpdater(Protocol):
    def update(self) -> None:
        pass


class IRenderer(Protocol):
    def render(self) -> PygameScreen:
        pass


class IEventHandler(Protocol):
    def try_handle_event(self, event: PygameEvent) -> bool:
        pass


class IModel(IEventHandler, Protocol):
    def get_action(self, state) -> int:
        pass


class IGameEnvironment(IEventHandler, Protocol):
    def step(self, action: Any, dt: float) -> Tuple[Any, bool]:
        pass

    def reset(self) -> None:
        pass

    def pop_events(self) -> List[Event]:
        pass

    def blit(self, screen) -> None:
        pass


class IScreen(Protocol):
    @property
    def size(self) -> Size:
        pass

    @property
    def alpha(self) -> int:
        pass

    @alpha.setter
    def alpha(self, value: int) -> None:
        pass

    def fill(self, color: Color, rect: Optional[Rect] = None) -> None:
        pass

    def blit(self, screen, shift: Shift) -> None:
        pass


class IFont(Protocol):
    def render(
        self,
        text: str,
        foreground_color: Color,
        background_color: Optional[Color],
        alpha: Optional[int],
    ) -> IScreen:
        pass

    def size(self, text: str) -> Size:
        pass


class IRenderKit(Protocol):
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
