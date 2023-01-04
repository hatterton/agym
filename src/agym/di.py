from typing import Mapping, Protocol, Type

from agym.dtos import (
    BreakoutCollisionEngine,
    BreakoutLevelType,
    Color,
    EnvironmentType,
    IOFrameworkType,
)
from agym.env_components.breakout import (
    BreakoutAudioHandler,
    BreakoutRenderer,
    KDTreeRenderer,
    ManualBreakoutModel,
)
from agym.env_components.many_breakouts import (
    ManyBreakoutsEnv,
    ManyBreakoutsEnvRender,
)
from agym.game_monitor import GameMonitor
from agym.io_frameworks import (
    AudioKit,
    FramerateClockDecorator,
    PygameIOFrameworkFactory,
    RenderKit,
)
from agym.main_window import MainWindow
from agym.protocols import (
    IClock,
    IEnvironmentAudioHandler,
    IEnvironmentModel,
    IRenderer,
    IRenderKit,
)
from agym.renderers import GameMonitorRenderer, TextLabel
from agym.settings import Settings
from agym.updaters import (
    ComposeUpdater,
    FPSUpdater,
    LimitedUpdater,
    ProfileUpdater,
)
from envs.breakout import (
    CollisionDetector,
    DefaultLevelBuilder,
    KDTreeCollisionDetectionEngine,
    NaiveCollisionDetectionEngine,
    PerformanceLevelBuilder,
)
from envs.breakout.protocols import (
    IBreakoutLevelBuilder,
    ICollisionDetectorEngine,
)
from envs.protocols import IGameEnvironment
from timeprofiler import TimeProfiler


class IOFramework:
    def __init__(self, config: Settings):
        type2framework_factory = {
            IOFrameworkType.PYGAME: PygameIOFrameworkFactory(),
        }

        framework_factory = type2framework_factory[config.io_framework_type]

        framework_factory.init_framework()

        self.clock: IClock = framework_factory.create_clock(
            config.graphics_framerate
        )
        self.clock = FramerateClockDecorator(
            clock=self.clock,
            history_size=config.framerate_history_size,
        )

        self.event_source = framework_factory.create_event_source(self.clock)

        audio_kit_engine = framework_factory.create_audio_kit_engine()
        self.audio_kit = AudioKit(engine=audio_kit_engine)

        render_kit_engine = framework_factory.create_render_kit_engine()
        self.render_kit = RenderKit(engine=render_kit_engine)


class TimeContainer:
    def __init__(self):
        self.time_profiler = TimeProfiler(
            window_size=10000,
            log_self=False,
        )


class Labels:
    def __init__(self, render_kit: IRenderKit, config: Settings):
        self.fps_label = TextLabel(
            render_kit=render_kit,
            font=render_kit.create_font("Hack", 12),
            foreground_color=Color(230, 230, 130),
            text="",
        )

        self.profile_label = TextLabel(
            render_kit=render_kit,
            font=render_kit.create_font("Hack", 12),
            foreground_color=Color(180, 130, 180),
            text="",
        )


class Updaters:
    def __init__(
        self,
        time_container: TimeContainer,
        clock: IClock,
        labels: Labels,
        config: Settings,
    ):
        self.fps_updater = FPSUpdater(
            label=labels.fps_label,
            clock=clock,
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
            clock=clock,
            ups=config.log_framerate,
        )


class IEnvContainer(Protocol):
    def __init__(self, io_framework: IOFramework, config: Settings) -> None:
        pass

    env: IGameEnvironment
    renderer: IRenderer
    audio_handler: IEnvironmentAudioHandler
    model: IEnvironmentModel


class BreakoutContainer(IEnvContainer):
    def __init__(self, io_framework: IOFramework, config: Settings):
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
        level_builder = level_type2level_builder[config.breakout.level_type]

        engine_type2engine: Mapping[
            BreakoutCollisionEngine, ICollisionDetectorEngine
        ] = {
            BreakoutCollisionEngine.NAIVE: NaiveCollisionDetectionEngine(),
            BreakoutCollisionEngine.KDTREE: KDTreeCollisionDetectionEngine(),
        }
        collision_detector_engine = engine_type2engine[
            config.breakout.collision_engine
        ]
        collision_detector = CollisionDetector(
            engine=collision_detector_engine,
        )

        self.env = ManyBreakoutsEnv(
            n=config.breakout.num_envs,
            env_size=config.breakout.env_size,
            collision_detector=collision_detector,
            level_builder=level_builder,
        )

        self.model = ManualBreakoutModel()
        self.audio_handler = BreakoutAudioHandler(
            audio_kit=io_framework.audio_kit
        )

        kdtree_renderer = KDTreeRenderer(
            screen_size=config.subenv_screen_size,
            render_kit=io_framework.render_kit,
        )

        breakout_renderer = BreakoutRenderer(
            screen_size=config.subenv_screen_size,
            kdtree_renderer=kdtree_renderer,
            render_kit=io_framework.render_kit,
            rendering_kdtree=config.rendering_kdtree,
            image_dir=config.breakout.image_dir,
        )

        self.renderer = ManyBreakoutsEnvRender(
            screen_size=config.env_screen_size,
            env=self.env,
            env_render=breakout_renderer,
            render_kit=io_framework.render_kit,
        )


class GameMonitorContainer:
    def __init__(
        self,
        io_framework: IOFramework,
        labels: Labels,
        updaters: Updaters,
        config: Settings,
    ):
        env_type2env_container: Mapping[
            EnvironmentType, Type[IEnvContainer]
        ] = {
            EnvironmentType.BREAKOUT: BreakoutContainer,
        }
        env_container = env_type2env_container[config.environment_type](
            io_framework=io_framework,
            config=config,
        )

        self.monitor = GameMonitor(
            clock=io_framework.clock,
            log_updater=updaters.log_updater,
            audio_handler=env_container.audio_handler,
            env=env_container.env,
            model=env_container.model,
            tps=config.tps,
        )

        self.renderer = GameMonitorRenderer(
            fps_label=labels.fps_label,
            profile_label=labels.profile_label,
            screen_size=config.window_screen_size,
            env_renderer=env_container.renderer,
            render_kit=io_framework.render_kit,
        )


class Windows:
    def __init__(
        self,
        game_monitor_container: GameMonitorContainer,
        io_framework: IOFramework,
        config: Settings,
    ):
        self.main = MainWindow(
            window_size=config.window_screen_size,
            render_kit=io_framework.render_kit,
            event_source=io_framework.event_source,
            game_monitor=game_monitor_container.monitor,
            game_monitor_renderer=game_monitor_container.renderer,
        )


class Application:
    def __init__(self, config: Settings):
        self.io_framework = IOFramework(config=config)

        self.time_container = TimeContainer()

        self.labels = Labels(
            render_kit=self.io_framework.render_kit, config=config
        )
        self.updaters = Updaters(
            time_container=self.time_container,
            clock=self.io_framework.clock,
            labels=self.labels,
            config=config,
        )

        self.game_monitor_container = GameMonitorContainer(
            io_framework=self.io_framework,
            labels=self.labels,
            updaters=self.updaters,
            config=config,
        )

        self.windows = Windows(
            game_monitor_container=self.game_monitor_container,
            io_framework=self.io_framework,
            config=config,
        )
