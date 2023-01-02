from agym.games.breakout.protocols import ILevelBuilder
from agym.games.breakout.state import BreakoutState

from .item_manager import ItemManager


class EmptyLevelBuilder(ILevelBuilder):
    def __init__(self) -> None:
        self._item_manager = ItemManager()

    def build(self) -> BreakoutState:
        return self._item_manager.extract_state()
