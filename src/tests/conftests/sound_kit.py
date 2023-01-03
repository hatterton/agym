import pytest

from agym.audio_kit import PygameSoundKitEngine, SoundKit


@pytest.fixture
def sound_kit_engine():
    return PygameSoundKitEngine()


@pytest.fixture
def sound_kit(sound_kit_engine):
    return SoundKit(engine=sound_kit_engine)
