from typing import Protocol

from .audio import IAudioKitEngine
from .clock import IClock
from .event import IEventSource
from .render import IRenderKitEngine


class IIOFrameworkFactory(Protocol):
    def create_clock(self, target_framerate: float) -> IClock:
        pass

    def create_event_source(self, clock: IClock) -> IEventSource:
        pass

    def create_audio_kit_engine(self) -> IAudioKitEngine:
        pass

    def create_render_kit_engine(self) -> IRenderKitEngine:
        pass

    def init_framework(self) -> None:
        pass
