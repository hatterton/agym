from agym.protocols import ISound, ISoundKit, ISoundKitEngine


class SoundKit(ISoundKit):
    def __init__(self, engine: ISoundKitEngine) -> None:
        self._engine = engine

    def load_sound(self, path: str) -> ISound:
        return self._engine.load_sound(path)
