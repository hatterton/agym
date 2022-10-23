import pytest
import pygame


@pytest.fixture
def init_pygame():
    pygame.init()
    pygame.font.init()



