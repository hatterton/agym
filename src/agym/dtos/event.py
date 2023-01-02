from dataclasses import dataclass

from envs.protocols import IGameEvent

from .key import Key


@dataclass
class Event:
    timestamp: float


@dataclass
class KeyboardEvent(Event):
    key: Key


@dataclass
class KeyDownEvent(KeyboardEvent):
    pass


@dataclass
class KeyUpEvent(KeyboardEvent):
    pass


@dataclass
class GameEvent(Event):
    source_event: IGameEvent


@dataclass
class QuitEvent(Event):
    pass
