from typing import Iterable, Optional

import pygame as pg

from agym.dtos import Event, Key, KeyCode, KeyDownEvent, KeyUpEvent
from agym.protocols import IClock, IEventSource


class PygameEventSource(IEventSource):
    def __init__(self, clock: IClock) -> None:
        self._clock = clock

        self._pygame2code = {
            # letters
            pg.K_a: KeyCode.A,
            pg.K_b: KeyCode.B,
            pg.K_c: KeyCode.C,
            pg.K_d: KeyCode.D,
            pg.K_e: KeyCode.E,
            pg.K_f: KeyCode.F,
            pg.K_g: KeyCode.G,
            pg.K_h: KeyCode.H,
            pg.K_i: KeyCode.I,
            pg.K_j: KeyCode.J,
            pg.K_k: KeyCode.K,
            pg.K_l: KeyCode.L,
            pg.K_m: KeyCode.M,
            pg.K_n: KeyCode.N,
            pg.K_o: KeyCode.O,
            pg.K_p: KeyCode.P,
            pg.K_q: KeyCode.Q,
            pg.K_r: KeyCode.R,
            pg.K_s: KeyCode.S,
            pg.K_t: KeyCode.T,
            pg.K_u: KeyCode.U,
            pg.K_v: KeyCode.V,
            pg.K_w: KeyCode.W,
            pg.K_x: KeyCode.X,
            pg.K_y: KeyCode.Y,
            pg.K_z: KeyCode.Z,
            # digits
            pg.K_0: KeyCode.D0,
            pg.K_1: KeyCode.D1,
            pg.K_2: KeyCode.D2,
            pg.K_3: KeyCode.D3,
            pg.K_4: KeyCode.D4,
            pg.K_5: KeyCode.D5,
            pg.K_6: KeyCode.D6,
            pg.K_7: KeyCode.D7,
            pg.K_8: KeyCode.D8,
            pg.K_9: KeyCode.D9,
            # punctuations
            pg.K_COMMA: KeyCode.COMMA,
            pg.K_PERIOD: KeyCode.PERIOD,
            pg.K_MINUS: KeyCode.MINUS,
            pg.K_PLUS: KeyCode.PLUS,
            pg.K_COLON: KeyCode.COLON,
            pg.K_SEMICOLON: KeyCode.SEMICOLON,
            pg.K_LEFTPAREN: KeyCode.LEFTPAREN,
            pg.K_RIGHTPAREN: KeyCode.RIGHTPAREN,
            pg.K_SLASH: KeyCode.SLASH,
            pg.K_QUESTION: KeyCode.QUESTION,
            pg.K_EXCLAIM: KeyCode.EXCLAIM,
            pg.K_QUOTE: KeyCode.QUOTE,
            pg.K_QUOTEDBL: KeyCode.DOUBLE_QUOTE,
            # arrows
            pg.K_LEFT: KeyCode.LEFT_ARROW,
            pg.K_RIGHT: KeyCode.RIGHT_ARROW,
            pg.K_UP: KeyCode.UP_ARROW,
            pg.K_DOWN: KeyCode.DOWN_ARROW,
            # controls
            pg.K_LCTRL: KeyCode.CONTROL,
            pg.K_RCTRL: KeyCode.CONTROL,
            pg.K_LSHIFT: KeyCode.SHIFT,
            pg.K_RSHIFT: KeyCode.SHIFT,
            # other
            pg.K_SPACE: KeyCode.SPACE,
            pg.K_BACKSPACE: KeyCode.BACKSPACE,
            pg.K_ESCAPE: KeyCode.ESCAPE,
        }

    def get_events(self) -> Iterable[Event]:
        event: Event

        current_time = self._clock.get_global_time()

        events = []
        for pg_event in pg.event.get():
            if pg_event.type == pg.KEYDOWN:
                key = self._try_extract_key(pg_event)
                if key is None:
                    continue

                event = KeyDownEvent(timestamp=current_time, key=key)

            elif pg_event.type == pg.KEYUP:
                key = self._try_extract_key(pg_event)
                if key is None:
                    continue

                event = KeyUpEvent(timestamp=current_time, key=key)

            else:
                continue

            events.append(event)

        return events

    def _try_extract_key(self, event: pg.event.Event) -> Optional[Key]:
        if event.key in self._pygame2code:
            return Key(
                code=self._pygame2code[event.key],
                unicode=event.unicode,
            )

        return None
