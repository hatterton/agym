from agym.audio_handler import AudioHandler
from agym.dtos import Color, Shift
from agym.game_monitor import GameMonitor
from agym.games import BreakoutEnv, ManualBreakoutModel
from agym.games.breakout import (
    BreakoutEnv,
    CollisionDetector,
    KDTreeCollisionDetectionEngine,
    NaiveCollisionDetectionEngine,
)
from agym.games.breakout.levels import (
    DefaultLevelBuilder,
    PerformanceLevelBuilder,
)
from agym.gui import TextLabel
from agym.main_window import MainWindow
from agym.protocols import IGameEnvironment, IModel
from agym.settings import Settings
from agym.updaters import (
    ComposeUpdater,
    FPSUpdater,
    LimitedUpdater,
    ProfileUpdater,
)
from agym.utils import FPSLimiter, TimeProfiler, register_profiler


class TimeContainer:
    def __init__(self, config: Settings):
        self.fps_limiter = FPSLimiter(
            max_fps=config.max_fps,
            history_size=1000,
        )
        self.time_profiler = TimeProfiler(
            window_size=10000,
            log_self=False,
        )


class Labels:
    def __init__(self, config: Settings):
        self.fps_label = TextLabel(
            shift=Shift(x=10, y=10),
            font_size=12,
            foreground_color=Color(230, 230, 130),
            text="fps",
        )

        self.profile_label = TextLabel(
            shift=Shift(x=120, y=10),
            font_size=12,
            foreground_color=Color(180, 130, 180),
            text="profiling",
        )


class Updaters:
    def __init__(
        self, time_container: TimeContainer, labels: Labels, config: Settings
    ):
        self.fps_updater = FPSUpdater(
            label=labels.fps_label,
            fps_limiter=time_container.fps_limiter,
        )

        self.profile_updater = ProfileUpdater(
            label=labels.profile_label,
            profiler=time_container.time_profiler,
        )

        self.compose_updater = ComposeUpdater(
            updaters=[
                self.fps_updater,
                self.profile_updater,
            ],
        )

        self.log_updater = LimitedUpdater(
            updater=self.compose_updater,
            ups=config.log_fps,
        )


class EnvContainer:
    def __init__(self, config: Settings):
        self.level_builder = DefaultLevelBuilder(
            # self.level_builder = PerformanceLevelBuilder(
            env_width=config.env_width,
            env_height=config.env_height,
            ball_speed=config.ball_speed,
            platform_speed=config.platform_speed,
        )

        # self.collision_detector_engine = NaiveCollisionDetectionEngine()
        self.collision_detector_engine = KDTreeCollisionDetectionEngine()

        self.collision_detector = CollisionDetector(
            engine=self.collision_detector_engine,
        )

        self.env = BreakoutEnv(
            env_width=config.env_width,
            env_height=config.env_height,
            collision_detector=self.collision_detector,
            level_builder=self.level_builder,
        )

        self.model = ManualBreakoutModel()
        self.audio_handler = AudioHandler()


class GameMonitorContainer:
    def __init__(
        self,
        time_container: TimeContainer,
        labels: Labels,
        env_container: EnvContainer,
        updaters: Updaters,
        config: Settings,
    ):
        self.game_monitor = GameMonitor(
            width=config.window_screen_width,
            height=config.window_screen_width,
            fps_limiter=time_container.fps_limiter,
            fps_label=labels.fps_label,
            profile_label=labels.profile_label,
            log_updater=updaters.log_updater,
            audio_handler=env_container.audio_handler,
            env=env_container.env,
            model=env_container.model,
            time_profiler=time_container.time_profiler,
            tps=config.tps,
        )


class Windows:
    def __init__(
        self, game_monitor_container: GameMonitorContainer, config: Settings
    ):
        self.main = MainWindow(
            width=config.window_screen_width,
            height=config.window_screen_height,
            game_monitor=game_monitor_container.game_monitor,
        )


class Application:
    def __init__(self, config: Settings):
        self.time_container = TimeContainer(config=config)
        self.labels = Labels(config=config)
        self.updaters = Updaters(
            time_container=self.time_container,
            labels=self.labels,
            config=config,
        )

        self.env_container = EnvContainer(config=config)

        self.game_monitor_container = GameMonitorContainer(
            time_container=self.time_container,
            labels=self.labels,
            env_container=self.env_container,
            updaters=self.updaters,
            config=config,
        )
        self.windows = Windows(
            game_monitor_container=self.game_monitor_container, config=config
        )
