from typing import List, Protocol

from envs.protocols import IGameEvent


class ISound(Protocol):
    def play(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> None:
        pass

    @property
    def volume(self) -> float:
        pass

    @volume.setter
    def volume(self, value: float) -> None:
        pass


class IAudioKitEngine(Protocol):
    def load_sound(self, path: str) -> ISound:
        pass


class IAudioKit(IAudioKitEngine, Protocol):
    pass


class IEnvironmentAudioHandler(Protocol):
    def play_background(self) -> None:
        pass

    def handle_events(self, events: List[IGameEvent]) -> None:
        pass
