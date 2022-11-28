from dataclasses import dataclass, field

from ..shapes import Rectangle, Shape

Id = int
ItemId = Id
ClassId = Id


@dataclass
class Record:
    item_id: ItemId
    class_id: ClassId
    shape: Shape
    bounding_box: Rectangle
