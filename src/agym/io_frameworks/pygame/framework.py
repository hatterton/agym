import pygame as pg

from agym.protocols import IClock, IIOFrameworkFactory

from .audio_kit import PygameAudioKitEngine
from .clock import PygameClock
from .event_source import PygameEventSource
from .render_kit import PygameRenderKitEngine


class PygameIOFrameworkFactory(IIOFrameworkFactory):
    def create_clock(self, target_framerate: float) -> PygameClock:
        return PygameClock(target_framerate)

    def create_event_source(self, clock: IClock) -> PygameEventSource:
        return PygameEventSource(clock)

    def create_audio_kit_engine(self) -> PygameAudioKitEngine:
        return PygameAudioKitEngine()

    def create_render_kit_engine(self) -> PygameRenderKitEngine:
        return PygameRenderKitEngine()

    def init_framework(self) -> None:
        pg.init()
        pg.font.init()
