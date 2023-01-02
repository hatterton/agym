import pytest

from agym.event_sources import PygameEventSource


@pytest.fixture
def event_source(clock):
    return PygameEventSource(clock)
