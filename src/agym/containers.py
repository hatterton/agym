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
from agym.main_window import MainWindow
from agym.utils import (
    FPSLimiter,
)


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()

    fps_limiter = providers.Factory(
        FPSLimiter,
        config.max_fps,
    )

    breakout = providers.Factory(
        BreakoutEnv,
        env_width=config.env_width,
        env_height=config.env_height,
        map_shape=[6, 6],
    )

    model = providers.Singleton(
        ManualBreakoutModel,
    )

    game_monitor = providers.Factory(
        GameMonitor,
        width=config.env_width,
        height=config.env_height,
        fps_limiter=fps_limiter,
        env=breakout,
        model=model,
    )

    main_window = providers.Factory(
        MainWindow,
        width=config.window_screen_width,
        height=config.window_screen_height,
        game_monitor=game_monitor,
    )


def create_app() -> Application:
    settings = Settings()

    app = Application()
    app.config.from_pydantic(settings)

    return app


def run_app(application: Application) -> None:
    application.main_window().run()
