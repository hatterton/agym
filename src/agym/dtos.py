from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Tuple

import pygame as pg


@dataclass
class Color:
    red: int
    green: int
    blue: int
    alpha: Optional[int] = None

    def to_tuple(self) -> Tuple[int, int, int, int]:
        if self.alpha is None:
            return (self.red, self.green, self.blue, 255)
        else:
            return (self.red, self.green, self.blue, self.alpha)


@dataclass
class Shift:
    x: int
    y: int

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


@dataclass
class Shape:
    width: int
    height: int

    def to_tuple(self) -> Tuple[int, int]:
        return self.width, self.height


@dataclass
class Event:
    timestamp: float


Screen = pg.surface.Surface
Rect = pg.rect.Rect
Font = pg.font.Font
PygameEvent = pg.event.Event
