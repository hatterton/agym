from agym.games.breakout.protocols import ILevelBuilder
from agym.games.breakout.state import GameState

from .item_manager import ItemManager


class EmptyLevelBuilder(ILevelBuilder):
    def __init__(self) -> None:
        self._item_manager = ItemManager()

    def build(self) -> GameState:
        return self._item_manager.extract_state()
