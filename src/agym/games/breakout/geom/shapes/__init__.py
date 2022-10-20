from typing import Union

from .rectangle import Rectangle
from .triangle import Triangle
from .circle import Circle

Shape = Union[Triangle, Circle, Rectangle]
