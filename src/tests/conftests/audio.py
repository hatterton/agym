import pytest

from agym.audio_handler import AudioHandler


@pytest.fixture
def audio_handler(sound_kit):
    return AudioHandler(sound_kit=sound_kit)
