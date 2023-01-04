from agym.protocols import IAudioKit, IAudioKitEngine, ISound


class AudioKit(IAudioKit):
    def __init__(self, engine: IAudioKitEngine) -> None:
        self._engine = engine

    def load_sound(self, path: str) -> ISound:
        return self._engine.load_sound(path)
