from typing import Tuple
import pygame

Color = Tuple[int, int, int]

class TextLabel:
    def __init__(self, x: int, y: int, font_size: int = 20, color: Color = (230, 230, 130), text: str = ""):
        self.shift = (x, y)

        self.color = color
        self.font_size = font_size
        self.font = pygame.font.SysFont("Hack", self.font_size)

        self.text: str = text

    def blit(self, screen) -> None:
        line_height = self.font_size
        for idx, text_line in enumerate(self.text.split("\n")):
            text_line_image = self.font.render(text_line, True, self.color)
            shift = (self.shift[0], self.font_size * idx + self.shift[1])
            screen.blit(text_line_image, shift)
