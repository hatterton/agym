from agym.audio_handler import AudioHandler
from agym.dtos import Color, Shift, Size
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
from agym.gui.render_kits import PygameRenderKitEngine, RenderKit
from agym.main_window import MainWindow
from agym.protocols import IGameEnvironment, IModel
from agym.renderers import EnvRenderer, GameMonitorRenderer, KDTreeRenderer
from agym.settings import Settings
from agym.updaters import (
    ComposeUpdater,
    FPSUpdater,
    LimitedUpdater,
    ProfileUpdater,
)
from agym.utils import FPSLimiter, TimeProfiler, register_profiler


class RenderKits:
    def __init__(self):
        self.pygame_render_kit_engine = PygameRenderKitEngine()

        self.kit = RenderKit(engine=self.pygame_render_kit_engine)


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
    def __init__(self, render_kits: RenderKits, config: Settings):
        kit = render_kits.kit

        self.fps_label = TextLabel(
            render_kit=kit,
            font=kit.create_font("Hack", 12),
            foreground_color=Color(230, 230, 130),
            text="",
        )

        self.profile_label = TextLabel(
            render_kit=kit,
            font=kit.create_font("Hack", 12),
            foreground_color=Color(180, 130, 180),
            text="",
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
        # self.level_builder = PerformanceLevelBuilder(
        self.level_builder = DefaultLevelBuilder(
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
            tps=config.tps,
        )


class Renderers:
    def __init__(
        self,
        game_monitor_container: GameMonitorContainer,
        env_container: EnvContainer,
        render_kits: RenderKits,
        config: Settings,
        labels: Labels,
    ):
        self.env_renderer = EnvRenderer(
            screen_size=Size(width=config.env_width, height=config.env_height),
            env=env_container.env,
            render_kit=render_kits.kit,
            image_dir=config.image_dir,
        )

        self.game_monitor = GameMonitorRenderer(
            fps_label=labels.fps_label,
            profile_label=labels.profile_label,
            screen_size=Size(
                width=config.window_screen_width,
                height=config.window_screen_height,
            ),
            env_renderer=self.env_renderer,
            render_kit=render_kits.kit,
        )


class Windows:
    def __init__(
        self,
        game_monitor_container: GameMonitorContainer,
        render_kits: RenderKits,
        renderers: Renderers,
        config: Settings,
    ):
        self.main = MainWindow(
            window_size=Size(
                width=config.window_screen_width,
                height=config.window_screen_height,
            ),
            render_kit=render_kits.kit,
            game_monitor=game_monitor_container.game_monitor,
            game_monitor_renderer=renderers.game_monitor,
        )


class Application:
    def __init__(self, config: Settings):
        self.render_kits = RenderKits()

        self.time_container = TimeContainer(config=config)
        self.labels = Labels(render_kits=self.render_kits, config=config)
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

        self.renderers = Renderers(
            game_monitor_container=self.game_monitor_container,
            env_container=self.env_container,
            labels=self.labels,
            render_kits=self.render_kits,
            config=config,
        )

        self.windows = Windows(
            game_monitor_container=self.game_monitor_container,
            config=config,
            render_kits=self.render_kits,
            renderers=self.renderers,
        )
