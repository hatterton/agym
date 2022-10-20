from enum import Enum
from typing import (
    Iterable,
)

from agym.games.breakout.geom import (
    KDTree,
    Record,
    ClassId,
    ItemId,
)
from agym.games.breakout.state import GameState
from agym.games.breakout.items import (
    Item,
    Platform,
    Ball,
    Block,
)
from agym.games.breakout.collisions import (
    Collision,
    CollisionBallBlock,
    CollisionBallPlatform,
    CollisionBallWall,
    CollisionPlatformWall,
    CollisionBallBall,
)
from agym.utils import CachedCollection

from .dtos import Collision


class ItemClass(Enum):
    WALL = 0
    BLOCK = 1
    BALL = 2
    PLATFORM = 3


class KDTreeCollisionDetectorEngine:
    def __init__(self) -> None:
        # self._collidable_pairs = {
        #     (ItemClass.WALL.value, ItemClass.BALL.value),
        #     (ItemClass.WALL.value, ItemClass.PLATFORM.value),
        #     (ItemClass.BLOCK.value, ItemClass.BALL.value),
        #     (ItemClass.BALL.value, ItemClass.BALL.value),
        #     (ItemClass.BALL.value, ItemClass.PLATFORM.value),
        # }
        self._class2class_id = {
            Ball: ItemClass.BALL.value,
            Block: ItemClass.BLOCK.value,
            Platform: ItemClass.PLATFORM.value,
        }

    def generate_step_collisions(self, state: GameState, dt: float) -> Iterable[Collision]:
        return CachedCollection(self._generate_step_collisions(state, dt))

    def _generate_step_collisions(self, state: GameState, dt: float) -> Iterable[Collision]:

        items = list(state.get_items())
        item_id2item = {idx: item for idx, item in enumerate(items)}
        item_id2item_class = {
            idx: self._class2class_id[type(item)]
            for idx, item in enumerate(items)
        }

        records = []
        for item_id, item in enumerate(items):
            for shape in item.get_ghost_trace(dt):
                records.append(
                    Record(
                        item_id=item_id,
                        class_id=item_id2item_class[item_id],
                        shape=shape,
                        bounding_box=shape.bounding_box,
                    )
                )

        tree = KDTree(
            records=records,
            alpha=0.5,
        )

        # print("Start")
        for (item_id1, item_id2), point in tree.generate_colliding_items():
            class_id1 = item_id2item_class[item_id1]
            class_id2 = item_id2item_class[item_id2]
            # print((class_id1, class_id2))

            if class_id1 > class_id2:
                item_id1, item_id2 = item_id2, item_id1
                class_id1, class_id2 = class_id2, class_id1

            # if not self._is_collidable(class_id1, class_id2):
            #     continue

            if (class_id1 == ItemClass.WALL.value and
                class_id2 == ItemClass.BALL.value):
                yield CollisionBallWall(
                    point=point,
                    ball=item_id2item[item_id2],
                )

            elif (class_id1 == ItemClass.WALL.value and
                  class_id2 == ItemClass.PLATFORM.value):
                yield CollisionPlatformWall(
                    point=point,
                    platform=item_id2item[item_id2],
                )

            elif (class_id1 == ItemClass.BLOCK.value and
                  class_id2 == ItemClass.BALL.value):
                yield CollisionBallBlock(
                    point=point,
                    block=item_id2item[item_id1],
                    ball=item_id2item[item_id2],
                )

            elif (class_id1 == ItemClass.BALL.value and
                  class_id2 == ItemClass.BALL.value):
                yield CollisionBallBall(
                    point=point,
                    ball1=item_id2item[item_id1],
                    ball2=item_id2item[item_id2],
                )

            elif (class_id1 == ItemClass.BALL.value and
                  class_id2 == ItemClass.PLATFORM.value):
                yield CollisionBallPlatform(
                    point=point,
                    ball=item_id2item[item_id1],
                    platform=item_id2item[item_id2],
                )


    # def _is_collidable(self, idx1: ClassId, idx2: ClassId) -> bool:
    #     return (idx1, idx2) in self._collidable_pairs
