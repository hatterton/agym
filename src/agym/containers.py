from dependency_injector import (
    containers,
    providers,
)

from agym.settings import Settings
from agym.game_monitor import GameMonitor
from agym.games import (
    IGameEnviroment,
    BreakoutEnv,
    ManualBreakoutModel,
)
from agym.utils import (
    FPSLimiter,
)


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()

    fps_limiter = providers.Singleton(
        FPSLimiter,
        config.max_fps,
    )

    breakout = providers.Singleton(
        BreakoutEnv,
        config.env_width,
        config.env_height,
        map_shape=[6, 6],
    )

    model = providers.Singleton(
        ManualBreakoutModel,
    )

    game_monitor = providers.Singleton(
        GameMonitor,
        window_screen_height=config.window_screen_height,
        window_screen_width=config.window_screen_width,
        env_width=config.env_width,
        env_height=config.env_height,
        fps_limiter=fps_limiter,
        env=breakout,
        model=model,
    )


def create_app() -> Application:
    settings = Settings()

    app = Application()
    app.config.from_pydantic(settings)

    return app


def run_app(application: Application) -> None:
    application.game_monitor().run()
