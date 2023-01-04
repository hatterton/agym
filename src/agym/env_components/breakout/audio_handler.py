from typing import List

from agym.protocols import IAudioKit, IEnvironmentAudioHandler
from envs.breakout import BreakoutCollisionEvent, CollisionBallBlock
from envs.protocols import IGameEvent


class BreakoutAudioHandler(IEnvironmentAudioHandler):
    def __init__(self, audio_kit: IAudioKit) -> None:
        self._audio_kit = audio_kit
        self._ball_brick_sound = self._audio_kit.load_sound(
            "../static/envs/breakout/sounds/trimmed_ball_brick_mono.wav"
        )
        self._backgroung_sound = self._audio_kit.load_sound(
            "../static/envs/breakout/sounds/death_note_shinigami_kai.mp3"
        )
        self._backgroung_sound.volume = 0.2

    def play_background(self) -> None:
        self._backgroung_sound.play(loops=-1)

    def handle_events(self, events: List[IGameEvent]) -> None:
        for event in events:
            if isinstance(event, BreakoutCollisionEvent):
                if isinstance(event.collision, CollisionBallBlock):
                    self._ball_brick_sound.play(maxtime=150, fade_ms=50)
