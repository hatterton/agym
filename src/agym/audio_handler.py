from typing import cast, List

from pygame.mixer import Sound

from agym.games.breakout.events import Event, CollisionEvent
from agym.games.breakout.dtos import EventType, CollisionType


class AudioHandler:
    def __init__(self) -> None:
        self.ball_brick_sound = Sound("agym/static/sounds/trimmed_ball_brick.wav")

    def handle_events(self, events: List[Event]) -> None:
        for event in events:
            if event.type == EventType.COLLISION:
                event = cast(CollisionEvent, event)

                if event.collision_type == CollisionType.BALL_BLOCK:
                    self.ball_brick_sound.play(maxtime=150, fade_ms=50)
