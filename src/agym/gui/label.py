import pygame
from typing import Callable
from abc import abstractmethod, ABC

class AbstractLabel(ABC):
    def __init__(self, x: int, y: int):
        self.shift = (x, y)

        self.color = (230, 230, 130)
        self.font_size = 24
        self.font = pygame.font.SysFont(None, self.font_size)

        self.text: str

        self.update()

    @abstractmethod
    def update(self) -> None:
        pass

    def blit(self, screen) -> None:
        line_height = self.font_size
        for idx, text_line in enumerate(self.text.split("\n")):
            text_line_image = self.font.render(text_line, True, self.color)
            shift = (self.shift[0], self.font_size * idx + self.shift[1])
            screen.blit(text_line_image, shift)
