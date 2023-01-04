from agym.dtos import Color, Rect, Size
from agym.env_components.breakout import BreakoutRenderer
from agym.protocols import IRenderer, IRenderKit, IScreen

from .env import ManyBreakoutsEnv


class ManyBreakoutsEnvRender(IRenderer):
    def __init__(
        self,
        screen_size: Size,
        env: ManyBreakoutsEnv,
        env_render: BreakoutRenderer,
        render_kit: IRenderKit,
    ) -> None:
        self._env = env
        self._env_render = env_render

        self._render_kit = render_kit
        self._screen_size = screen_size

        self._split_color = Color(150, 150, 150)

    def render(self) -> IScreen:
        screen = self._render_kit.create_screen(self._screen_size)

        num_envs = len(self._env.envs)

        n = 1
        while n * n < num_envs:
            n += 1

        for i, env in enumerate(self._env.envs):
            row = i // n
            col = i % n

            env_rect = Rect.from_sides(
                left=col * self._screen_size.width // n,
                right=(col + 1) * self._screen_size.width // n,
                top=row * self._screen_size.width // n,
                bottom=(row + 1) * self._screen_size.width // n,
            )

            self._env_render.env = env
            env_screen = self._env_render.render()
            env_screen = env_screen.resize(env_rect.size)

            screen.blit(env_screen, env_rect.shift)

        return screen
