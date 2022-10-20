from typing import Protocol

from .shapes import Rectangle


class SupportsBoundingBox(Protocol):
    @property
    def bounding_box(self) -> Rectangle:
        pass

