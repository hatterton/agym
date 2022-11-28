from typing import Union

from .circle import Circle
from .rectangle import Rectangle
from .triangle import Triangle

Shape = Union[Triangle, Circle, Rectangle]
