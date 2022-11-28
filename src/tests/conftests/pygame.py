import pygame
import pytest


@pytest.fixture
def init_pygame():
    pygame.init()
    pygame.font.init()
