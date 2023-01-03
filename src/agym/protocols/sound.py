from typing import Protocol


class ISound(Protocol):
    def play(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> None:
        pass

    @property
    def volume(self) -> float:
        pass

    @volume.setter
    def volume(self, value: float) -> None:
        pass


class ISoundKitEngine(Protocol):
    def load_sound(self, path: str) -> ISound:
        pass


class ISoundKit(ISoundKitEngine, Protocol):
    pass
