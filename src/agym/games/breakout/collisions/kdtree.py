from enum import Enum, auto
from typing import Iterable, cast

from agym.games.breakout.dtos import (
    Ball,
    Block,
    Collision,
    CollisionBallBall,
    CollisionBallBlock,
    CollisionBallPlatform,
    CollisionBallWall,
    CollisionPlatformWall,
    Item,
    Platform,
    Wall,
)
from agym.games.breakout.geom import ClassId, ItemId, KDTree, Record
from agym.games.breakout.state import GameState
from agym.utils import CachedCollection

from .precise import calculate_ball_ball_colls


class ItemClass(Enum):
    BALL = auto()
    BLOCK = auto()
    PLATFORM = auto()
    WALL = auto()


class KDTreeCollisionDetectionEngine:
    def __init__(self) -> None:
        self._class2class_id = {
            Ball: ItemClass.BALL.value,
            Block: ItemClass.BLOCK.value,
            Platform: ItemClass.PLATFORM.value,
            Wall: ItemClass.WALL.value,
        }

        self._collidable_pairs = {
            (ItemClass.BALL.value, ItemClass.BALL.value),
            (ItemClass.BALL.value, ItemClass.BLOCK.value),
            (ItemClass.BALL.value, ItemClass.PLATFORM.value),
            (ItemClass.BALL.value, ItemClass.WALL.value),
            (ItemClass.PLATFORM.value, ItemClass.WALL.value),
        }

    def generate_step_collisions(
        self, state: GameState, dt: float
    ) -> Iterable[Collision]:
        return CachedCollection(self._generate_step_collisions(state, dt))

    def _generate_step_collisions(
        self, state: GameState, dt: float
    ) -> Iterable[Collision]:

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
            collidable_pairs=self._collidable_pairs,
            max_depth=10,
            num_records_stop=1,
        )

        for (item_id1, item_id2), point in tree.generate_colliding_items():
            class_id1 = item_id2item_class[item_id1]
            class_id2 = item_id2item_class[item_id2]

            if (
                class_id1 == ItemClass.BALL.value
                and class_id2 == ItemClass.BALL.value
            ):

                ball1 = cast(Ball, item_id2item[item_id1])
                ball2 = cast(Ball, item_id2item[item_id2])

                coll = calculate_ball_ball_colls(ball1, ball2, dt)

                if coll is not None:
                    yield CollisionBallBall(
                        point=point,
                        ball1=ball1,
                        ball2=ball2,
                    )

            elif (
                class_id1 == ItemClass.BALL.value
                and class_id2 == ItemClass.BLOCK.value
            ):
                yield CollisionBallBlock(
                    point=point,
                    ball=cast(Ball, item_id2item[item_id1]),
                    block=cast(Block, item_id2item[item_id2]),
                )

            elif (
                class_id1 == ItemClass.BALL.value
                and class_id2 == ItemClass.PLATFORM.value
            ):
                yield CollisionBallPlatform(
                    point=point,
                    ball=cast(Ball, item_id2item[item_id1]),
                    platform=cast(Platform, item_id2item[item_id2]),
                )

            elif (
                class_id1 == ItemClass.BALL.value
                and class_id2 == ItemClass.WALL.value
            ):
                yield CollisionBallWall(
                    point=point,
                    ball=cast(Ball, item_id2item[item_id1]),
                    wall=cast(Wall, item_id2item[item_id2]),
                )

            elif (
                class_id1 == ItemClass.PLATFORM.value
                and class_id2 == ItemClass.WALL.value
            ):
                yield CollisionPlatformWall(
                    point=point,
                    platform=cast(Platform, item_id2item[item_id1]),
                    wall=cast(Wall, item_id2item[item_id2]),
                )
