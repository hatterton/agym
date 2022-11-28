from typing import List, cast

from pygame.mixer import Sound

from agym.games.breakout.dtos import CollisionBallBlock, CollisionEvent, Event


class AudioHandler:
    def __init__(self) -> None:
        self.ball_brick_sound = Sound(
            "agym/static/sounds/trimmed_ball_brick.wav"
        )

    def handle_events(self, events: List[Event]) -> None:
        for event in events:
            if isinstance(event, CollisionEvent):
                if isinstance(event.collision, CollisionBallBlock):
                    self.ball_brick_sound.play(maxtime=150, fade_ms=50)
