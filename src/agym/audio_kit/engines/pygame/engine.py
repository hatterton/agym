import pygame as pg

from agym.protocols import ISoundKitEngine

from .sound import PygameSound


class PygameSoundKitEngine(ISoundKitEngine):
    def load_sound(self, path: str) -> PygameSound:
        pg_sound = pg.mixer.Sound(path)
        sound = PygameSound(pg_sound)
        return sound
