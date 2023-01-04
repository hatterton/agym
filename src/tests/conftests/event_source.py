import pytest


@pytest.fixture
def event_source(io_framework_factory, clock):
    return io_framework_factory.create_event_source(clock)
