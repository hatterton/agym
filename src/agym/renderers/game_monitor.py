from agym.dtos import Color, Shift, Size
from agym.game_monitor import GameMonitor
from agym.gui import TextLabel
from agym.protocols import IRenderer, IRenderKit, IScreen
from agym.utils import TimeProfiler, profile

from .env import EnvRenderer


class GameMonitorRenderer(IRenderer):
    def __init__(
        self,
        screen_size: Size,
        env_renderer: EnvRenderer,
        fps_label: TextLabel,
        profile_label: TextLabel,
        render_kit: IRenderKit,
    ):
        self._env_renderer = env_renderer
        self._fps_label = fps_label
        self._profile_label = profile_label

        self._render_kit = render_kit
        self._screen_size = screen_size

    @profile("game_render")
    def render(self) -> IScreen:
        screen = self._render_kit.create_screen(self._screen_size)

        screen.fill(Color(0, 0, 0))

        env_screen = self._env_renderer.render()
        env_rect = env_screen.rect
        env_rect.bottom = screen.rect.bottom
        env_rect.centerx = screen.rect.centerx
        screen.blit(env_screen, env_rect.shift)

        screen.blit(self._fps_label.render(), Shift(x=10, y=10))
        screen.blit(self._profile_label.render(), Shift(x=120, y=10))

        return screen
