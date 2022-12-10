from agym.dtos import Size
from agym.protocols import IRenderer, IRenderKit, IScreen


class EmptyRenderer(IRenderer):
    def __init__(
        self,
        render_kit: IRenderKit,
    ):
        self._render_kit = render_kit

    def render(self) -> IScreen:
        screen = self._render_kit.create_screen(Size(1, 1))

        return screen
