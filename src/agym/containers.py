import pygame

from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Singleton,
    Factory,
    List as pList,
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
from agym.updaters import (
    FPSUpdater,
    ProfileUpdater,
    ComposeUpdater,
    LimitedUpdater,
)
from agym.audio_handler import AudioHandler
from agym.gui import TextLabel
from agym.utils import (
    TimeProfiler,
    register_profiler,
)


class Application(DeclarativeContainer):
    config = Configuration()

    fps_limiter = Singleton(
        FPSLimiter,
        max_fps=config.max_fps,
        history_size=4000,
    )
    time_profiler = Singleton(
        TimeProfiler,
        window_size=10000,
        log_self=False,
    )


    fps_label = Singleton(
        TextLabel,
        x=10,
        y=10,
        font_size=12,
        text="fps",
    )
    profile_label = Singleton(
        TextLabel,
        x=120,
        y=10,
        font_size=12,
        color=(180, 130, 180),
        text="profiling",
    )

    fps_updater = Singleton(
        FPSUpdater,
        label=fps_label,
        fps_limiter=fps_limiter,
    )
    profile_updater = Singleton(
        ProfileUpdater,
        label=profile_label,
        profiler=time_profiler,
    )
    compose_updater = Singleton(
        ComposeUpdater,
        updaters=pList(
            fps_updater,
            profile_updater,
        ),
    )
    log_updater = Singleton(
        LimitedUpdater,
        updater=compose_updater,
        ups=config.log_fps,
    )

    breakout = Singleton(
        BreakoutEnv,
        env_width=config.env_width,
        env_height=config.env_height,
        ball_speed=config.ball_speed,
        platform_speed=config.platform_speed,
    )

    model = Singleton(
        ManualBreakoutModel,
    )

    audio_handler = Singleton(
        AudioHandler,
    )

    game_monitor = Singleton(
        GameMonitor,
        width=config.window_screen_width,
        height=config.window_screen_width,
        fps_limiter=fps_limiter,
        fps_label=fps_label,
        profile_label=profile_label,
        log_updater=log_updater,
        audio_handler=audio_handler,
        env=breakout,
        model=model,
        time_profiler=time_profiler,
        tps=config.tps,
    )

    main_window = Singleton(
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
