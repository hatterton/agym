import pygame as pg

from agym.protocols import ISound


class PygameSound(ISound):
    def __init__(self, sound: pg.mixer.Sound) -> None:
        self._sound = sound

    def play(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> None:
        self._sound.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)

    @property
    def volume(self) -> float:
        return self._sound.get_volume()

    @volume.setter
    def volume(self, value: float) -> None:
        self._sound.set_volume(value)
