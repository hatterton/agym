import pytest

from agym.io_frameworks import AudioKit


@pytest.fixture
def audio_kit_engine(io_framework_factory):
    return io_framework_factory.create_audio_kit_engine()


@pytest.fixture
def audio_kit(audio_kit_engine):
    return AudioKit(engine=audio_kit_engine)
