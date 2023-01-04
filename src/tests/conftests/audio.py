import pytest

from agym.env_components.breakout import BreakoutAudioHandler


@pytest.fixture
def audio_handler(audio_kit):
    return BreakoutAudioHandler(audio_kit=audio_kit)
