import pygame

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
from agym.labels import FPSLabel
from agym.audio_handler import AudioHandler


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()

    fps_limiter = providers.Singleton(
        FPSLimiter,
        config.max_fps,
    )
    fps_label = providers.Factory(
        FPSLabel,
        x=10,
        y=10,
        fps_limiter=fps_limiter,
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

    audio_handler = providers.Singleton(
        AudioHandler,
    )

    game_monitor = providers.Singleton(
        GameMonitor,
        width=config.window_screen_width,
        height=config.window_screen_width,
        fps_limiter=fps_limiter,
        fps_label=fps_label,
        audio_handler=audio_handler,
        env=breakout,
        model=model,
    )

    main_window = providers.Singleton(
        MainWindow,
        width=config.window_screen_width,
        height=config.window_screen_height,
        game_monitor=game_monitor,
    )


def create_app() -> Application:
    pygame.init()
    pygame.font.init()

    settings = Settings()

    app = Application()
    app.config.from_pydantic(settings)

    return app


def run_app(application: Application) -> None:
    application.main_window().run()
