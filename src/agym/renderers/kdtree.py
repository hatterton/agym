from typing import Dict, List, Mapping, Optional

from agym.dtos import Color, Rect, Shift, Size
from agym.games import BreakoutEnv
from agym.games.breakout.collisions import KDTreeBuilder
from agym.games.breakout.geom import (
    ClassId,
    ItemId,
    KDTree,
    LeafTreeNode,
    ParentRelativeType,
    Record,
    Rectangle,
    SplitTreeNode,
    TreeNode,
    TreeNodeType,
)
from agym.protocols import IRenderer, IRenderKit, IScreen


class KDTreeRenderer(IRenderer):
    def __init__(
        self,
        screen_size: Size,
        env: BreakoutEnv,
        render_kit: IRenderKit,
    ):
        self._env = env

        self._render_kit = render_kit
        self._screen_size = screen_size

        self._width = 1

        self._middle_color = Color(150, 0, 0)
        self._leaf_color = Color(0, 150, 0)
        self._threshold_color = Color(150, 150, 150)

        self._kdtree_font = self._render_kit.create_font("Hack", 12)

    def _convert_rectangle_to_rect(self, rect: Rectangle) -> Rect:
        return Rect.from_sides(
            left=int(rect.left),
            top=int(rect.top),
            right=int(rect.right),
            bottom=int(rect.bottom),
        )

    def render(self) -> IScreen:
        screen = self._render_kit.create_screen(self._screen_size)

        state = self._env.state
        tree = KDTreeBuilder(state.get_items()).build(1e-4)

        self._render_node_on(
            screen=screen,
            node=tree.root,
        )

        return screen

    def _render_node_on(
        self,
        screen: IScreen,
        node: TreeNode,
        segment_rect: Optional[Rect] = None,
        parent: Optional[SplitTreeNode] = None,
    ) -> None:
        if segment_rect is None:
            segment_rect = self._convert_rectangle_to_rect(node.bounding_box)

        if isinstance(node, SplitTreeNode):
            self._render_subnodes_on(
                screen=screen,
                node=node,
                segment_rect=segment_rect,
            )

            self._render_node_threshold_on(
                screen=screen,
                node=node,
                color=self._threshold_color,
                segment_rect=segment_rect,
            )

        if node.parent_relative == ParentRelativeType.ROOT:
            self._render_node_box_on(
                screen=screen,
                node=node,
                color=self._threshold_color,
            )

        if node.parent_relative == ParentRelativeType.MIDDLE:
            self._render_node_box_on(
                screen=screen,
                node=node,
                color=self._middle_color,
            )

        if node.is_leaf:
            self._render_node_box_on(
                screen=screen,
                node=node,
                color=self._leaf_color,
            )

    def _render_node_box_on(
        self,
        screen: IScreen,
        node: TreeNode,
        color: Color,
    ) -> None:
        node_rect = self._convert_rectangle_to_rect(node.bounding_box)

        self._render_kit.draw_rect(
            screen=screen,
            rect=node_rect,
            color=color,
            width=self._width,
        )

    def _render_node_threshold_on(
        self,
        screen: IScreen,
        node: SplitTreeNode,
        color: Color,
        segment_rect: Rect,
    ) -> None:
        threshold = int(node.threashold)

        if node.type == TreeNodeType.VERTICAL:
            self._render_kit.draw_line(
                screen=screen,
                start=Shift(x=segment_rect.left, y=threshold),
                finish=Shift(x=segment_rect.right, y=threshold),
                color=color,
                width=self._width,
            )

        elif node.type == TreeNodeType.HORISONTAL:
            self._render_kit.draw_line(
                screen=screen,
                start=Shift(x=threshold, y=segment_rect.top),
                finish=Shift(x=threshold, y=segment_rect.bottom),
                color=color,
                width=self._width,
            )

    def _render_subnodes_on(
        self,
        screen: IScreen,
        node: SplitTreeNode,
        segment_rect: Rect,
    ) -> None:

        threshold = int(node.threashold)
        if node.type == TreeNodeType.HORISONTAL:
            left_segment_rect = Rect.from_sides(
                left=segment_rect.left,
                top=segment_rect.top,
                right=threshold,
                bottom=segment_rect.bottom,
            )

            right_segment_rect = Rect.from_sides(
                left=threshold,
                top=segment_rect.top,
                right=segment_rect.right,
                bottom=segment_rect.bottom,
            )

        else:
            left_segment_rect = Rect.from_sides(
                left=segment_rect.left,
                top=segment_rect.top,
                right=segment_rect.right,
                bottom=threshold,
            )

            right_segment_rect = Rect.from_sides(
                left=segment_rect.left,
                top=threshold,
                right=segment_rect.right,
                bottom=segment_rect.bottom,
            )

        if node.left is not None:
            self._render_node_on(
                screen=screen,
                node=node.left,
                segment_rect=left_segment_rect,
                parent=node,
            )

        if node.right is not None:
            self._render_node_on(
                screen=screen,
                node=node.right,
                segment_rect=right_segment_rect,
                parent=node,
            )
