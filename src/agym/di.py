from typing import Mapping

from agym.audio_handler import AudioHandler
from agym.clocks import FramerateClockDecorator, PygameClock
from agym.dtos import (
    BreakoutCollisionEngine,
    BreakoutLevelType,
    Color,
    Shift,
    Size,
)
from agym.event_sources import PygameEventSource
from agym.game_models import ManualBreakoutModel
from agym.game_monitor import GameMonitor
from envs.breakout import (
    BreakoutEnv,
    CollisionDetector,
    KDTreeCollisionDetectionEngine,
    NaiveCollisionDetectionEngine,
)
from envs.breakout import (
    DefaultLevelBuilder,
    PerformanceLevelBuilder,
)
from envs.breakout.protocols import (
    IBreakoutLevelBuilder,
    ICollisionDetectorEngine,
)
from envs.protocols import IGameEnvironment
from agym.gui import TextLabel
from agym.gui.render_kits import PygameRenderKitEngine, RenderKit
from agym.main_window import MainWindow
from agym.many_breakouts import ManyBreakoutsEnv
from agym.protocols import IModel
from agym.renderers import (
    EmptyRenderer,
    EnvRenderer,
    GameMonitorRenderer,
    KDTreeRenderer,
    ManyBreakoutsEnvRender,
)
from agym.settings import Settings
from agym.updaters import (
    ComposeUpdater,
    FPSUpdater,
    LimitedUpdater,
    ProfileUpdater,
)
from timeprofiler import TimeProfiler, register_profiler
from geometry import Vec2


class RenderKits:
    def __init__(self):
        self.pygame_render_kit_engine = PygameRenderKitEngine()

        self.kit = RenderKit(engine=self.pygame_render_kit_engine)


class Clocks:
    def __init__(self, config: Settings):
        self.pygame = PygameClock(
            target_framerate=config.graphics_framerate,
        )

        clock = self.pygame

        self.framerate_decorated = FramerateClockDecorator(
            clock=clock,
            history_size=config.framerate_history_size,
        )

        self.clock = self.framerate_decorated


class EventSources:
    def __init__(
        self,
        clocks: Clocks,
    ):
        self.pygame = PygameEventSource(
            clock=clocks.clock,
        )

        self.event_source = self.pygame


class TimeContainer:
    def __init__(self):
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
        self,
        time_container: TimeContainer,
        clocks: Clocks,
        labels: Labels,
        config: Settings,
    ):
        self.fps_updater = FPSUpdater(
            label=labels.fps_label,
            clock=clocks.clock,
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
            clock=clocks.clock,
            ups=config.log_framerate,
        )


class EnvContainer:
    def __init__(self, config: Settings):

        level_type2level_builder: Mapping[
            BreakoutLevelType, IBreakoutLevelBuilder
        ] = {
            BreakoutLevelType.PERFORMANCE: PerformanceLevelBuilder(
                env_size=config.breakout.env_size,
                num_balls=config.breakout.num_balls,
                ball_speed=config.breakout.ball_speed,
                ball_radius=config.breakout.ball_radius,
            ),
            BreakoutLevelType.DEFAULT: DefaultLevelBuilder(
                env_size=config.breakout.env_size,
                ball_speed=config.breakout.ball_speed,
                ball_radius=config.breakout.ball_radius,
                platform_speed=config.breakout.platform_speed,
                platform_size=config.breakout.platform_size,
                block_wall_num_rows=config.breakout.block_wall_num_rows,
                block_size=config.breakout.block_size,
                block_wall_top_shift=config.breakout.block_wall_top_shift,
                block_wall_between_shift=config.breakout.block_wall_between_shift,
            ),
        }

        self.level_builder = level_type2level_builder[
            config.breakout.level_type
        ]

        engine_type2engine: Mapping[
            BreakoutCollisionEngine, ICollisionDetectorEngine
        ] = {
            BreakoutCollisionEngine.NAIVE: NaiveCollisionDetectionEngine(),
            BreakoutCollisionEngine.KDTREE: KDTreeCollisionDetectionEngine(),
        }
        self.collision_detector_engine = engine_type2engine[
            config.breakout.collision_engine
        ]

        self.collision_detector = CollisionDetector(
            engine=self.collision_detector_engine,
        )

        self.env = ManyBreakoutsEnv(
            n=config.breakout.num_envs,
            env_size=config.breakout.env_size,
            collision_detector=self.collision_detector,
            level_builder=self.level_builder,
        )

        self.model: IModel = ManualBreakoutModel()
        self.audio_handler = AudioHandler()


class GameMonitorContainer:
    def __init__(
        self,
        clocks: Clocks,
        env_container: EnvContainer,
        updaters: Updaters,
        config: Settings,
    ):
        self.game_monitor = GameMonitor(
            clock=clocks.clock,
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

        self.empty = EmptyRenderer(
            render_kit=render_kits.kit,
        )

        self.kdtree = KDTreeRenderer(
            screen_size=config.subenv_screen_size,
            render_kit=render_kits.kit,
        )

        self.breakout_env = EnvRenderer(
            screen_size=config.subenv_screen_size,
            kdtree_renderer=self.kdtree,
            render_kit=render_kits.kit,
            rendering_kdtree=config.rendering_kdtree,
            image_dir=config.breakout.image_dir,
        )

        self.env = ManyBreakoutsEnvRender(
            screen_size=config.env_screen_size,
            env=env_container.env,
            env_render=self.breakout_env,
            render_kit=render_kits.kit,
        )

        self.game_monitor = GameMonitorRenderer(
            fps_label=labels.fps_label,
            profile_label=labels.profile_label,
            screen_size=config.window_screen_size,
            env_renderer=self.env,
            render_kit=render_kits.kit,
        )


class Windows:
    def __init__(
        self,
        game_monitor_container: GameMonitorContainer,
        render_kits: RenderKits,
        renderers: Renderers,
        event_sources: EventSources,
        config: Settings,
    ):
        self.main = MainWindow(
            window_size=config.window_screen_size,
            render_kit=render_kits.kit,
            event_source=event_sources.event_source,
            game_monitor=game_monitor_container.game_monitor,
            game_monitor_renderer=renderers.game_monitor,
        )


class Application:
    def __init__(self, config: Settings):
        self.render_kits = RenderKits()

        self.time_container = TimeContainer()
        self.clocks = Clocks(config=config)
        self.event_sources = EventSources(clocks=self.clocks)

        self.labels = Labels(render_kits=self.render_kits, config=config)
        self.updaters = Updaters(
            time_container=self.time_container,
            clocks=self.clocks,
            labels=self.labels,
            config=config,
        )

        self.env_container = EnvContainer(config=config)

        self.game_monitor_container = GameMonitorContainer(
            clocks=self.clocks,
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
            event_sources=self.event_sources,
            renderers=self.renderers,
        )
