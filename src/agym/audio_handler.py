from typing import List

from pygame.mixer import Sound

from envs.breakout import BreakoutCollisionEvent, CollisionBallBlock
from envs.protocols import IGameEvent


class AudioHandler:
    def __init__(self) -> None:
        self._ball_brick_sound = Sound(
            "../static/envs/breakout/sounds/trimmed_ball_brick_mono.wav"
        )

    def handle_events(self, events: List[IGameEvent]) -> None:
        for event in events:
            if isinstance(event, BreakoutCollisionEvent):
                if isinstance(event.collision, CollisionBallBlock):
                    self._ball_brick_sound.play(maxtime=150, fade_ms=50)
