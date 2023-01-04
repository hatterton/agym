import pygame as pg

from agym.protocols import IAudioKitEngine

from .sound import PygameSound


class PygameAudioKitEngine(IAudioKitEngine):
    def load_sound(self, path: str) -> PygameSound:
        pg_sound = pg.mixer.Sound(path)
        sound = PygameSound(pg_sound)
        return sound
