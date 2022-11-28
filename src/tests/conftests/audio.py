import pytest

from agym.audio_handler import AudioHandler


@pytest.fixture
def audio_handler():
    return AudioHandler()
